from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_customers.models import ZohoCustomer 
from django.utils.dateparse import parse_datetime  
import requests
import json
import os

def list_customers(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)
    print(headers)
    url = f'{settings.ZOHO_URL_READ_CUSTOMERS}?organization_id={app_config.zoho_org_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        customers = response.json()
        for customer in customers.get('contacts'):
            data = json.loads(customer) if isinstance(customer, str) else customer
            new_customer = create_customer_instance(data) 
            new_customer.save()
        context = {
            'customers': ZohoCustomer.objects.all() 
        }  
        return render(request, 'api_zoho_customers/list_customers.html', context)
    else:
        return JsonResponse({"error": "Failed to fetch invoices"}), response.status_code
    

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
