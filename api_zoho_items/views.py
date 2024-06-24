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
    url = f'{settings.ZOHO_URL_READ_ITEMS}?organization_id={app_config.zoho_org_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
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
    item.unit = data.get('unit')
    item.status = data.get('status')
    item.source = data.get('source', 'csv')
    item.is_linked_with_zohocrm = data.get('is_linked_with_zohocrm', False)
    item.zcrm_product_id = data.get('zcrm_product_id', '')
    item.description = data.get('description', '')
    item.rate = data.get('rate', 0.0)
    item.tax_id = data.get('tax_id', '')
    item.tax_name = data.get('tax_name', '')
    item.tax_percentage = data.get('tax_percentage', 0)
    item.purchase_account_id = data.get('purchase_account_id')
    item.purchase_account_name = data.get('purchase_account_name')
    item.account_id = data.get('account_id')
    item.account_name = data.get('account_name')
    item.purchase_description = data.get('purchase_description', '')
    item.purchase_rate = data.get('purchase_rate', 0.0)
    item.item_type = data.get('item_type')
    item.product_type = data.get('product_type')
    item.stock_on_hand = data.get('stock_on_hand', 0.0)
    item.has_attachment = data.get('has_attachment', False)
    item.available_stock = data.get('available_stock', 0.0)
    item.actual_available_stock = data.get('actual_available_stock', 0.0)
    item.sku = data.get('sku')
    item.reorder_level = data.get('reorder_level', '')
    item.image_name = data.get('image_name', '')
    item.image_type = data.get('image_type', '')
    item.image_document_id = data.get('image_document_id', '')
    item.created_time = parse_datetime(data.get('created_time'))
    item.last_modified_time = parse_datetime(data.get('last_modified_time'))
    item.cf_qb_ref_id = data.get('cf_qb_ref_id')
    item.cf_qb_ref_id_unformatted = data.get('cf_qb_ref_id_unformatted')
    return item