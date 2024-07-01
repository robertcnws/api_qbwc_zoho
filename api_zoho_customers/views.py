from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_customers.models import ZohoCustomer 
from django.utils.dateparse import parse_datetime  
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_customers(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)  # Asegúrate de que esto esté configurado correctamente
    params = {
        'page': 1,       # Página inicial
        'per_page': 200  # Cantidad de resultados por página, ajusta según la API de Zoho
    }
    url = f'{settings.ZOHO_URL_READ_CUSTOMERS}?organization_id={app_config.zoho_org_id}'
    customers_to_save = []
    customers_saved = ZohoCustomer.objects.all()
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:  # Si el token ha expirado
                new_token = api_zoho_views.refresh_zoho_token()
                headers['Authorization'] = f'Zoho-oauthtoken {new_token}'
                response = requests.get(url, headers=headers, params=params)  # Reintenta la solicitud
            response.raise_for_status()
            customers = response.json()
            
            for customer in customers.get('contacts', []):
                data = json.loads(customer) if isinstance(customer, str) else customer
                new_customer = create_customer_instance(data)
                value = list(filter(lambda x: x.contact_id == new_customer.contact_id, customers_saved))
                if len(value) == 0 and new_customer.status == 'active':
                    customers_to_save.append(new_customer)
            
            if 'page_context' in customers and 'has_more_page' in customers['page_context'] and customers['page_context']['has_more_page']:
                params['page'] += 1  # Avanza a la siguiente página
            else:
                break  # Sal del bucle si no hay más páginas
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching customers: {e}")
            return JsonResponse({"error": "Failed to fetch customers"}), 500
    
    for customer in customers_to_save:
        customer.save()  
    # Después de obtener todos los clientes, renderiza la plantilla con la lista de clientes
    customers_list = ZohoCustomer.objects.all()
    context = {'customers': customers_list}
    return render(request, 'api_zoho_customers/list_customers.html', context)
    

def create_customer_instance(data):
    customer = ZohoCustomer()
    customer.contact_id = data.get('contact_id')
    customer.contact_name = data.get('contact_name')
    customer.customer_name = data.get('customer_name')
    customer.company_name = data.get('company_name', '')
    customer.status = data.get('status')
    customer.first_name = data.get('first_name')
    customer.last_name = data.get('last_name')
    customer.email = data.get('email')
    customer.phone = data.get('phone', '')
    customer.mobile = data.get('mobile', '')
    customer.created_time = parse_datetime(data.get('created_time'))
    customer.created_time_formatted = data.get('created_time_formatted', '')
    customer.last_modified_time = parse_datetime(data.get('last_modified_time'))
    customer.last_modified_time_formatted = data.get('last_modified_time_formatted', '')
    return customer
