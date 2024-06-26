from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from api_zoho_customers.models import ZohoCustomer
from api_zoho_items.models import ZohoItem
from .models import QbItem
import difflib
import api_quickbook_soap.soap_service as soap_service
import xmltodict
import logging

# Configura el logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

counter = 0
soap_customers = []
soap_items = []
insert = False

@csrf_exempt
def item_query(request):
    global soap_items
    return start_qbwc_query_request(request, 'ItemInventory', soap_items)

@csrf_exempt
def customer_query(request):
    global soap_customers
    return start_qbwc_query_request(request, 'Customer', soap_customers)

def matching_items(request):
    global soap_items
    for item in soap_items:
        qb_item = QbItem.objects.create(list_id=item['ListID'], name=item['Name'])
        qb_item.save()
    qb_items = QbItem.objects.all()
    zoho_items = ZohoItem.objects.all()
    similar_items = []
    for qb_item in qb_items:    
        for zoho_item in zoho_items:
            seem = difflib.SequenceMatcher(None, qb_item.name, zoho_item.name).ratio()
            if seem > 0.5:
                similar_items.append(
                    {
                        'qb_item_list_id': qb_item.list_id, 
                        'qb_item_name': qb_item.name, 
                        'zoho_item': zoho_item.name, 
                        'seem': seem,
                        'coincidence': f'{round(seem * 100, 2)} %'
                    }
                )
    sorted_items = sorted(similar_items, key=lambda x: x['seem'], reverse=True)
    context = {'similar_items': sorted_items}
    return render(request, 'api_quickbook_soap/similar_items.html', context)
    
def start_qbwc_query_request(request, query_object_name, list_of_objects):
    if request.method == 'POST':
        xml_data = request.body.decode('utf-8')
        # logger.debug(f"Received XML data: {xml_data}")
        if f'{query_object_name}Ret' in xml_data:
            xml_dict = xmltodict.parse(xml_data)
            response_xml = xml_dict['soap:Envelope']['soap:Body']['receiveResponseXML']['response']
            data_dict = xmltodict.parse(response_xml)
            if f'{query_object_name}QueryRs' in xml_data:
                elements_query_rs = data_dict['QBXML']['QBXMLMsgsRs'][f'{query_object_name}QueryRs'][f'{query_object_name}Ret']
                list_of_objects = [elem for elem in elements_query_rs]
                print(f"SOAP Elements ({query_object_name}): {list_of_objects}")
                if query_object_name == 'ItemInventory':
                    for item in list_of_objects:
                        qb_item = QbItem.objects.create(list_id=item['ListID'], name=item['Name'])
                        qb_item.save()
        response_xml = process_qbwc_query_request(xml_data, query_object_name)
        return HttpResponse(response_xml, content_type='text/xml')
    else:
        return HttpResponse(status=405)

def partition_list_iter(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def process_qbwc_query_request(xml_data, query_object_name):
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
            if query_object_name == 'ItemInventory':
                response = soap_service.generate_item_query_response()
            else:
                response = soap_service.generate_customer_query_response()
            insert = True
        # elif 'sendRequestXML' in body and counter == 0 and insert:
        #     counter += 1
        #     # # insert = False
        #     # customers_to_add = sync_customers()
        #     # print(f"ZOHO Customers: {customers_to_add}")
        #     # response = soap_service.generate_customer_add_response_new_version(customers_to_add)
        #     # # chunk_size = 20 
        #     # # partitioned_list = list(partition_list_iter(customers_to_add, chunk_size))
        #     # # for chunk in partitioned_list:
        #     # #     response = soap_service.generate_customer_add_response(chunk)
        #     # #     return 
        #     items_to_add = sync_items()
        #     print(f"ZOHO Items: {items_to_add}")
        #     response = soap_service.generate_item_add_response(items_to_add)
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
    zoho_final_customers = list(filter(not_duplicate_customers, zoho_initial_customers))
    return zoho_final_customers

def not_duplicate_customers(zoho_customer):
    global soap_customers
    return all(zoho_customer.email != obj['Email'] for obj in soap_customers)

def sync_items():
    global soap_items
    zoho_initial_items = ZohoItem.objects.all()
    zoho_final_items = list(filter(not_duplicate_items, zoho_initial_items))
    return zoho_final_items

def not_duplicate_items(zoho_item):
    global soap_items
    return all((zoho_item.name != obj['Name'] and zoho_item.sku != obj['SKU']) for obj in soap_items)
    
