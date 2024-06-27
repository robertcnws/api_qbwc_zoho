from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from api_zoho_customers.models import ZohoCustomer
from api_zoho_items.models import ZohoItem
from api_zoho_items.forms import ZohoItemForm
from .models import QbItem, QbCustomer
from .forms import QbItemForm
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
similar_customers = []
similar_items = []
insert = False

#############################################
# Endpoints to Serve SOAP Requests

@csrf_exempt
def item_query(request):
    global soap_items
    return start_qbwc_query_request(request, 'ItemInventory', soap_items)

@csrf_exempt
def customer_query(request):
    global soap_customers
    return start_qbwc_query_request(request, 'Customer', soap_customers)


#############################################
# Home page module

def quickbook_api_settings(request):
    global soap_customers
    global soap_items
    return render(request, 'api_quickbook_soap/quickbook_api_settings.html')


#############################################
# Trying to get matched elements here

def matching_items(request):
    global soap_items
    global similar_items
    similar_items = []
    qb_items = QbItem.objects.filter(matched=False)
    zoho_items = ZohoItem.objects.filter(qb_list_id__isnull=True) | ZohoItem.objects.filter(qb_list_id='')
    for qb_item in qb_items:    
        dependences_list = []
        for zoho_item in zoho_items:
            seem = difflib.SequenceMatcher(None, qb_item.name, zoho_item.name).ratio() if qb_item.name and zoho_item.name else 0
            if seem > 0.4 and zoho_item.qb_list_id == '':
                dependence = {
                        'zoho_item_id': zoho_item.item_id,
                        'zoho_item': zoho_item.name, 
                        'zoho_item_sku': zoho_item.sku,
                        'seem': seem,
                        'coincidence': f'{round(seem * 100, 2)} %'
                }
                dependences_list.append(dependence)
        sorted_dependences_list = sorted(dependences_list, key=lambda x: x['seem'], reverse=True)
        similar_items.append({
                                'qb_item_list_id': qb_item.list_id, 
                                'qb_item_name': qb_item.name,
                                'coincidences_by_order': sorted_dependences_list
                            })
    context = {'similar_items': similar_items}
    return render(request, 'api_quickbook_soap/similar_items.html', context)


def matching_customers(request):
    global soap_customers
    global similar_customers
    qb_customers = QbCustomer.objects.filter(matched=False)
    zoho_customers = ZohoCustomer.objects.filter(qb_list_id__isnull=True) | ZohoCustomer.objects.filter(qb_list_id='')
    for qb_customer in qb_customers:    
        dependences_list = []
        for zoho_customer in zoho_customers:
            seem_email = difflib.SequenceMatcher(None, qb_customer.email, zoho_customer.email).ratio() if qb_customer.email and zoho_customer.email else 0
            seem_phone = difflib.SequenceMatcher(None, qb_customer.phone, zoho_customer.phone).ratio() if qb_customer.phone and zoho_customer.phone else 0
            if (seem_email > 0.7 or seem_phone > 0.7) and zoho_customer.qb_list_id == '':
                dependence = {
                        'zoho_customer_id': zoho_customer.contact_id,
                        'zoho_customer': zoho_customer.customer_name, 
                        'email': zoho_customer.email,
                        'seem_email': seem_email,
                        'coincidence_email': f'{round(seem_email * 100, 2)} %',
                        'phone': zoho_customer.phone,
                        'seem_phone': seem_phone,
                        'coincidence_phone': f'{round(seem_phone * 100, 2)} %'
                }
                dependences_list.append(dependence)
        sorted_dependences_list = sorted(dependences_list, key=lambda x: x['seem_email'], reverse=True)
        similar_customers.append({
                                'qb_customer_list_id': qb_customer.list_id, 
                                'qb_customer_name': qb_customer.name,
                                'qb_customer_name': qb_customer.name,
                                'qb_customer_email': qb_customer.email,
                                'qb_customer_phone': qb_customer.phone,
                                'coincidences_by_order': sorted_dependences_list
                            })
    context = {'similar_customers': similar_customers}
    return render(request, 'api_quickbook_soap/similar_customers.html', context)


#############################################
# Display matched elements


def matched_items(request):
    qb_items = QbItem.objects.filter(matched=True)
    zoho_items = ZohoItem.objects.filter(qb_list_id__isnull=False) | ZohoItem.objects.exclude(qb_list_id='')
    matched_items = []
    for qb_item in qb_items: 
        for zoho_item in zoho_items:
            if qb_item.list_id == zoho_item.qb_list_id:
                matched = {
                        'zoho_item_id': zoho_item.item_id,
                        'zoho_item': zoho_item.name, 
                        'zoho_item_sku': zoho_item.sku,
                        'qb_item_name': qb_item.name,
                        'qb_item_list_id': qb_item.list_id,
                        'zoho_item_qb_list_id': zoho_item.qb_list_id
                }
                if matched not in matched_items:
                    matched_items.append(matched)
    context = {'matched_items': matched_items}
    return render(request, 'api_quickbook_soap/matched_items.html', context)


def matched_customers(request):
    qb_customers = QbCustomer.objects.filter(matched=True)
    zoho_customers = ZohoCustomer.objects.filter(qb_list_id__isnull=False) | ZohoItem.objects.exclude(qb_list_id='')
    matched_customers = []
    for qb_customer in qb_customers: 
        for zoho_customer in zoho_customers:
            if qb_customer.list_id == zoho_customer.qb_list_id:
                matched = {
                        'zoho_customer_id': zoho_customer.item_id,
                        'zoho_customer': zoho_customer.customer_name, 
                        'qb_customer_name': qb_customer.name,
                        'qb_customer_list_id': qb_customer.list_id,
                        'zoho_customer_qb_list_id': zoho_customer.qb_list_id
                }
                if matched not in matched_customers:
                    matched_customers.append(matched)
    context = {'matched_customers': matched_customers}
    return render(request, 'api_quickbook_soap/matched_customers.html', context)


#############################################
# AJAX methods
#############################################
# Match all by first element

@require_POST
def match_all_first_items_ajax(request):
    global similar_items
    filter_similar_items = list(filter(lambda x: len(x['coincidences_by_order']) > 0, similar_items))
    action = request.GET.get('action')  
    try:
        for item in filter_similar_items:
            if item['coincidences_by_order']:
                zoho_item = ZohoItem.objects.get(item_id=item['coincidences_by_order'][0]['zoho_item_id'])
                qb_item = QbItem.objects.get(list_id=item['qb_item_list_id'])
                zoho_item.qb_list_id = item['qb_item_list_id'] if action == 'match' else ''
                zoho_item.save()
                qb_item.matched = True if action == 'match' else False
                qb_item.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@require_POST
def match_all_first_customers_ajax(request):
    global similar_customers
    filter_similar_customers = list(filter(lambda x: len(x['coincidences_by_order']) > 0, similar_customers))
    action = request.GET.get('action')  
    try:
        for customer in filter_similar_customers:
            if customer['coincidences_by_order']:
                zoho_customer = ZohoCustomer.objects.get(item_id=customer['coincidences_by_order'][0]['zoho_customer_id'])
                qb_customer = QbCustomer.objects.get(list_id=customer['qb_customer_list_id'])
                zoho_customer.qb_list_id = customer['qb_item_list_id'] if action == 'match' else ''
                zoho_customer.save()
                qb_customer.matched = True if action == 'match' else False
                qb_customer.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


#############################################
# Match one by selected element

@require_POST
def match_one_item_ajax(request):
    action = request.GET.get('action')  
    try:
        qb_list_id = request.POST['qb_item_list_id']
        zoho_item_id = request.POST['zoho_item_id']
        qb_item = get_object_or_404(QbItem, list_id=qb_list_id)
        zoho_item = get_object_or_404(ZohoItem, item_id=zoho_item_id)
        zoho_item.qb_list_id = qb_list_id if action == 'match' else ''
        zoho_item.save()
        qb_item.matched = True if action == 'match' else False
        qb_item.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

@require_POST
def match_one_customer_ajax(request):
    action = request.GET.get('action')
    try:
        qb_list_id = request.POST['qb_customer_list_id']
        zoho_customer_id = request.POST['zoho_customer_id']
        qb_customer = get_object_or_404(QbItem, list_id=qb_list_id)
        zoho_customer = get_object_or_404(ZohoCustomer, item_id=zoho_customer_id)
        zoho_customer.qb_list_id = qb_list_id if action == 'match' else ''
        zoho_customer.save()
        qb_customer.matched = True if action == 'match' else False
        qb_customer.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    
#############################################    
# SOAP requests

    
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
                        qb_item = QbItem.objects.create(
                            list_id=item['ListID'], 
                            name=item['Name'] if 'Name' in item else '',
                        )
                        qb_item.save()
                elif query_object_name == 'Customer':
                    for customer in list_of_objects:
                        qb_customer = QbCustomer.objects.create(
                            list_id=customer['ListID'], 
                            name=customer['FullName'] if 'FullName' in customer else '',  
                            email=customer['Email'] if 'Email' in customer else '', 
                            phone=customer['Phone'] if 'Phone' in customer else ''
                        )
                        qb_customer.save()
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
    
