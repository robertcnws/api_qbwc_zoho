from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_customers.models import ZohoCustomer 
from django.utils.dateparse import parse_datetime 
from django.contrib.auth.decorators import login_required
from django.db import transaction
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@login_required(login_url='login')
def list_customers(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)  # Asegúrate de que esto esté configurado correctamente
    customers_saved = list(ZohoCustomer.objects.all())

    params = {
        'page': 1,
        'per_page': 200,  # Asegúrate de que este sea el valor máximo permitido por la API
        'organization_id': app_config.zoho_org_id,
    }

    url = f'{settings.ZOHO_URL_READ_CUSTOMERS}'
    customers_to_save = []
    customers_to_get = [] 

    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:  # Si el token ha expirado
                new_token = api_zoho_views.refresh_zoho_token()
                headers['Authorization'] = f'Zoho-oauthtoken {new_token}'
                response = requests.get(url, headers=headers, params=params)  # Reintenta la solicitud
            response.raise_for_status()
            customers = response.json()
            if customers.get('contacts', []):
                customers_to_get.extend(customers['contacts'])
            if 'page_context' in customers and 'has_more_page' in customers['page_context'] and customers['page_context']['has_more_page']:
                params['page'] += 1  # Avanza a la siguiente página
            else:
                break  # Sal del bucle si no hay más páginas
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching customers: {e}")
            return JsonResponse({"error": "Failed to fetch customers"}, status=500)
    
    existing_customers = {customer.contact_id: customer for customer in customers_saved}
    existing_emails = {customer.email: customer for customer in customers_saved}

    for data in customers_to_get:
        new_customer = create_customer_instance(data)
        if new_customer.contact_id not in existing_customers and new_customer.email not in existing_emails and new_customer.status == 'active':
            customers_to_save.append(new_customer)

    def save_customers_in_batches(customers, batch_size=100):
        for i in range(0, len(customers), batch_size):
            batch = customers[i:i + batch_size]
            with transaction.atomic():
                ZohoCustomer.objects.bulk_create(batch)
    
    save_customers_in_batches(customers_to_save, batch_size=100)

    # Después de obtener todos los clientes, renderiza la plantilla con la lista de clientes
    customers_list_query = ZohoCustomer.objects.all()
    batch_size = 200  # Ajusta este tamaño según tus necesidades
    customers_list = []
    
    # Dividir en partes y procesar cada parte
    for i in range(0, customers_list_query.count(), batch_size):
        batch = customers_list_query[i:i + batch_size]
        customers_list.extend(batch)  # Agregar datos al acumulador
    
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
