from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api_zoho_customers.models import ZohoCustomer
import api_quickbook_soap.soap_service as soap_service
import xmltodict
import logging

# Configura el logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

counter = 0
soap_customers = []
insert = False

@csrf_exempt
def customer_query(request):
    global soap_customers
    if request.method == 'POST':
        xml_data = request.body.decode('utf-8')
        # logger.debug(f"Received XML data: {xml_data}")
        if 'CustomerRet' in xml_data:
            xml_dict = xmltodict.parse(xml_data)
            response_xml = xml_dict['soap:Envelope']['soap:Body']['receiveResponseXML']['response']
            data_dict = xmltodict.parse(response_xml)
            if 'CustomerQueryRs' in xml_data:
                customer_query_rs = data_dict['QBXML']['QBXMLMsgsRs']['CustomerQueryRs']['CustomerRet']
                soap_customers = [customer for customer in customer_query_rs]
                print(f"SOAP Customers: {soap_customers}")
        response_xml = process_qbwc_query_request(xml_data)
        return HttpResponse(response_xml, content_type='text/xml')
    else:
        return HttpResponse(status=405)

def partition_list_iter(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def process_qbwc_query_request(xml_data, list_of_customers=[]):
    global counter
    global soap_customers
    global insert
    response = None
    try:
        xml_dict = xmltodict.parse(xml_data)
        body = xml_dict['soap:Envelope']['soap:Body']
        if 'authenticate' in body:
            response = soap_service.handle_authenticate(body)
        elif 'sendRequestXML' in body and counter == 0 and not insert:
            response = soap_service.generate_customer_query_response()
            insert = True
        elif 'sendRequestXML' in body and counter == 0 and insert:
            counter += 1
            # insert = False
            customers_to_add = sync_customers()
            print(f"ZOHO Customers: {customers_to_add}")
            response = soap_service.generate_customer_add_response_new_version(customers_to_add)
            # chunk_size = 20 
            # partitioned_list = list(partition_list_iter(customers_to_add, chunk_size))
            # for chunk in partitioned_list:
            #     response = soap_service.generate_customer_add_response(chunk)
            #     return 
        elif 'closeConnection' in body:
            counter = 0
            response = soap_service.generate_close_connection_response()
        else:
            response = soap_service.generate_unsupported_request_response()
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return soap_service.generate_error_response(str(e))
    
def sync_customers():
    global soap_customers
    zoho_initial_customers = ZohoCustomer.objects.all()
    zoho_final_customers = list(filter(not_duplicate_object, zoho_initial_customers))
    return zoho_final_customers

def not_duplicate_object(zoho_customer):
    global soap_customers
    return all(zoho_customer.email != obj['Email'] for obj in soap_customers)
    
