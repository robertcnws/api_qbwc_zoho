from django.shortcuts import render
from django.http import JsonResponse
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_items.models import ZohoItem 
from django.utils.dateparse import parse_datetime 
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_items(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)  # Asegúrate de que esto esté configurado correctamente
    params = {
        'page': 1,       # Página inicial
        'per_page': 200  # Cantidad de resultados por página, ajusta según la API de Zoho
    }
    url = f'{settings.ZOHO_URL_READ_ITEMS}?organization_id={app_config.zoho_org_id}'
    items_to_save = []
    items_saved = ZohoItem.objects.all()
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:  # Si el token ha expirado
                new_token = api_zoho_views.refresh_zoho_token()
                headers['Authorization'] = f'Zoho-oauthtoken {new_token}'
                response = requests.get(url, headers=headers, params=params)  # Reintenta la solicitud
            response.raise_for_status()
            items = response.json()
            # logger.info(f'Items Page {params["page"]}: {items}')
            
            for item in items.get('items', []):
                data = json.loads(item) if isinstance(item, str) else item
                new_item = create_item_instance(data)
                value = list(filter(lambda x: x.item_id == new_item.item_id, items_saved))
                if len(value) == 0:
                    items_to_save.append(new_item)
            # Verifica si hay más páginas para obtener
            if 'page_context' in items and 'has_more_page' in items['page_context'] and items['page_context']['has_more_page']:
                params['page'] += 1  # Avanza a la siguiente página
            else:
                break  # Sal del bucle si no hay más páginas
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching customers: {e}")
            return JsonResponse({"error": "Failed to fetch customers"}), 500
    for item in items_to_save:
        value = list(filter(lambda x: x.item_id == item.item_id, items_saved))
        if len(value) == 0:
            item.save()  
    # Después de obtener todos los clientes, renderiza la plantilla con la lista de clientes
    items_list = ZohoItem.objects.all()
    
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