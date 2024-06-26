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

def list_invoices(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)
    url = f'{settings.ZOHO_URL_READ_INVOICES}?organization_id={app_config.zoho_org_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        api_zoho_views.refresh_token(request)
        headers = api_zoho_views.config_headers(request)
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            if response.status_code == 200:
                invoices = response.json()
                print(invoices)
                # for customer in items.get('contacts'):
                #     data = json.loads(customer) if isinstance(customer, str) else customer
                #     new_customer = create_customer_instance(data) 
                #     new_customer.save()
                context = {
                    'invoices': ZohoCustomer.objects.all() 
                }  
                # return invoices
                return render(request, 'api_zoho_invoices/list_invoices.html', context)
        except requests.exceptions.HTTPError as err:
                print(err)
                return JsonResponse({"error": "Failed to fetch invoices"}), response.status_code
    

def create_item_instance(data):
    customer = ZohoCustomer()
    customer.contact_id = data.get('contact_id')
    customer.contact_name = data.get('contact_name')
    customer.customer_name = data.get('customer_name')
    customer.vendor_name = data.get('vendor_name', '')
    customer.company_name = data.get('company_name', '')
    customer.website = data.get('website', '')
    customer.language_code = data.get('language_code', '')
    customer.language_code_formatted = data.get('language_code_formatted', '')
    customer.contact_type = data.get('contact_type')
    customer.contact_type_formatted = data.get('contact_type_formatted', '')
    customer.status = data.get('status')
    customer.customer_sub_type = data.get('customer_sub_type', '')
    customer.source = data.get('source', '')
    customer.is_linked_with_zohocrm = data.get('is_linked_with_zohocrm', False)
    customer.payment_terms = data.get('payment_terms', 0)
    customer.payment_terms_label = data.get('payment_terms_label')
    customer.currency_id = data.get('currency_id')
    customer.twitter = data.get('twitter', '')
    customer.facebook = data.get('facebook', '')
    customer.currency_code = data.get('currency_code')
    customer.outstanding_receivable_amount = data.get('outstanding_receivable_amount', 0.0)
    customer.outstanding_receivable_amount_bcy = data.get('outstanding_receivable_amount_bcy', 0.0)
    customer.outstanding_payable_amount = data.get('outstanding_payable_amount', 0.0)
    customer.outstanding_payable_amount_bcy = data.get('outstanding_payable_amount_bcy', 0.0)
    customer.unused_credits_receivable_amount = data.get('unused_credits_receivable_amount', 0.0)
    customer.unused_credits_receivable_amount_bcy = data.get('unused_credits_receivable_amount_bcy', 0.0)
    customer.unused_credits_payable_amount = data.get('unused_credits_payable_amount', 0.0)
    customer.unused_credits_payable_amount_bcy = data.get('unused_credits_payable_amount_bcy', 0.0)
    customer.first_name = data.get('first_name')
    customer.last_name = data.get('last_name')
    customer.email = data.get('email')
    customer.phone = data.get('phone', '')
    customer.mobile = data.get('mobile', '')
    customer.portal_status = data.get('portal_status')
    customer.portal_status_formatted = data.get('portal_status_formatted', '')
    customer.track_1099 = data.get('track_1099', False)
    customer.created_time = parse_datetime(data.get('created_time'))
    customer.created_time_formatted = data.get('created_time_formatted', '')
    customer.last_modified_time = parse_datetime(data.get('last_modified_time'))
    customer.last_modified_time_formatted = data.get('last_modified_time_formatted', '')
    customer.ach_supported = data.get('ach_supported', False)
    customer.has_attachment = data.get('has_attachment', False)
    return customer