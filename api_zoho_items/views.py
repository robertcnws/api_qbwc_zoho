from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_items.models import ZohoItem 
from django.utils.dateparse import parse_datetime 
from django.db import transaction
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@login_required(login_url='login')  
def list_items(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)
    items_saved = list(ZohoItem.objects.all())
    
    params = {
        'organization_id': app_config.zoho_org_id,
        'page': 1,       # Página inicial
        'per_page': 200,  # Cantidad de resultados por página
        'status': 'active'  # Solo items activos
    }
        
    url = f'{settings.ZOHO_URL_READ_ITEMS}'
    items_to_save = []
    items_to_get = []
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:  # Si el token ha expirado
                new_token = api_zoho_views.refresh_zoho_token()
                headers['Authorization'] = f'Zoho-oauthtoken {new_token}'
                response = requests.get(url, headers=headers, params=params)  # Reintenta la solicitud
            response.raise_for_status()
            items = response.json()
            if items.get('items', []):
                items_to_get.extend(items['items'])
            # Verifica si hay más páginas para obtener
            if 'page_context' in items and 'has_more_page' in items['page_context'] and items['page_context']['has_more_page']:
                params['page'] += 1  # Avanza a la siguiente página
            else:
                break  # Sal del bucle si no hay más páginas
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching items: {e}")
            return JsonResponse({"error": "Failed to fetch items"}, status=500)
    
    existing_items = {item.item_id: item for item in items_saved}

    for data in items_to_get:
        new_item = create_item_instance(data)
        if new_item.item_id not in existing_items:
            items_to_save.append(new_item)
    
    def save_items_in_batches(items, batch_size=100):
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            with transaction.atomic():
                ZohoItem.objects.bulk_create(batch)
    
    save_items_in_batches(items_to_save, batch_size=100)

    items_list_query = ZohoItem.objects.all()
    batch_size = 200  # Ajusta este tamaño según tus necesidades
    items_list = []
    
    # Dividir en partes y procesar cada parte
    for i in range(0, items_list_query.count(), batch_size):
        batch = items_list_query[i:i + batch_size]
        items_list.extend(batch)  
        
    context = {'items': items_list}
    return render(request, 'api_zoho_items/list_items.html', context)

    

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