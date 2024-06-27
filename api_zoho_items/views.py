from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_items.models import ZohoItem 
from django.utils.dateparse import parse_datetime 
import requests
import json
import os

def list_items(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)
    print(headers)
    url = f'{settings.ZOHO_URL_READ_ITEMS}?organization_id={app_config.zoho_org_id}'
    response = requests.get(url, headers=headers)
    # if response.status_code == 401:
    #     api_zoho_views.get_refresh_token(request)
    #     headers = api_zoho_views.config_headers(request)
    #     print(headers)
    #     response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.raise_for_status()
        items = response.json()
        print(items)
        for item in items.get('items'):
            data = json.loads(item) if isinstance(item, str) else item
            new_item = create_item_instance(data) 
            new_item.save()
        context = {
            'items': ZohoItem.objects.all() 
        }
        return render(request, 'api_zoho_items/list_items.html', context)
    else:
        return JsonResponse({"error": "Failed to fetch invoices"}), response.status_code
    

def create_item_instance(data):
    item = ZohoItem()
    item.item_id = data.get('item_id')
    item.name = data.get('name')
    item.item_name = data.get('item_name')
    item.status = data.get('status')
    item.description = data.get('description', '')
    item.rate = data.get('rate', 0.0)
    item.sku = data.get('sku')
    item.created_time = parse_datetime(data.get('created_time'))
    item.last_modified_time = parse_datetime(data.get('last_modified_time'))
    item.qb_list_id = data.get('cf_qb_ref_id')
    return item