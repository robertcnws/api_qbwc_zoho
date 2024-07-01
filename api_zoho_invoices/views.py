from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import make_aware
from datetime import datetime
import api_zoho.views as api_zoho_views
from django.conf import settings
from api_zoho.models import AppConfig   
from api_zoho_invoices.models import ZohoFullInvoice 
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_invoices(request):
    app_config = AppConfig.objects.first()
    headers = api_zoho_views.config_headers(request)
    params = {
        'page': 1,       # Página inicial
        'per_page': 200  # Cantidad de resultados por página, ajusta según la API de Zoho
    }
    url = f'{settings.ZOHO_URL_READ_INVOICES}?organization_id={app_config.zoho_org_id}'
    invoices_to_save = []
    invoices_saved = ZohoFullInvoice.objects.all()
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:  # Si el token ha expirado
                new_token = api_zoho_views.refresh_zoho_token()
                headers['Authorization'] = f'Zoho-oauthtoken {new_token}'
                response = requests.get(url, headers=headers, params=params)  # Reintenta la solicitud
            response.raise_for_status()
            invoices = response.json()
            
            for invoice in invoices.get('invoices', []):
                data = json.loads(invoice) if isinstance(invoice, str) else invoice
                get_url = f'{settings.ZOHO_URL_READ_INVOICES}/{data.get('invoice_id')}/?organization_id={app_config.zoho_org_id}'
                response = requests.get(get_url, headers=headers)
                if response.status_code == 200:
                    response.raise_for_status()
                    full_invoice = response.json()
                    data = json.loads(full_invoice.get('invoice')) if isinstance(full_invoice.get('invoice'), str) else full_invoice.get('invoice')
                    new_invoice = create_invoice_instance(data)
                    value = list(filter(lambda x: x.invoice_id == new_invoice.invoice_id, invoices_saved))
                    if len(value) == 0:
                        invoices_to_save.append(new_invoice)
            # Verifica si hay más páginas para obtener
            if 'page_context' in invoices and 'has_more_page' in invoices['page_context'] and invoices['page_context']['has_more_page']:
                params['page'] += 1  # Avanza a la siguiente página
            else:
                break  # Sal del bucle si no hay más páginas
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching customers: {e}")
            return JsonResponse({"error": "Failed to fetch customers"}), 500
    for invoice in invoices_to_save:
        value = list(filter(lambda x: x.invoice_id == invoice.invoice_id, invoices_saved))
        if len(value) == 0:
            invoice.save()  
    # Después de obtener todos los clientes, renderiza la plantilla con la lista de clientes
    invoice_list = ZohoFullInvoice.objects.all()
    context = {'invoices': invoice_list}
    return render(request, 'api_zoho_invoices/list_invoices.html', context)
    

def create_invoice_instance(data):
    try:
        instance = ZohoFullInvoice(
            invoice_id=data.get('invoice_id', ''),
            invoice_number=data.get('invoice_number', ''),
            date=parse_date(data.get('date')),
            due_date=parse_date(data.get('due_date')),
            offline_created_date_with_time=data.get('offline_created_date_with_time', ''),
            customer_id=data.get('customer_id', ''),
            customer_name=data.get('customer_name', ''),
            email=data.get('email', ''),
            currency_id=data.get('currency_id', ''),
            invoice_source=data.get('invoice_source', ''),
            currency_code=data.get('currency_code', ''),
            currency_symbol=data.get('currency_symbol', ''),
            currency_name_formatted=data.get('currency_name_formatted', ''),
            status=data.get('status', ''),
            recurring_invoice_id=data.get('recurring_invoice_id', ''),
            payment_terms=data.get('payment_terms', 0),
            payment_terms_label=data.get('payment_terms_label', ''),
            payment_reminder_enabled=data.get('payment_reminder_enabled', False),
            payment_discount=data.get('payment_discount', 0.0),
            credits_applied=data.get('credits_applied', 0.0),
            payment_made=data.get('payment_made', 0.0),
            zcrm_potential_id=data.get('zcrm_potential_id', ''),
            zcrm_potential_name=data.get('zcrm_potential_name', ''),
            reference_number=data.get('reference_number', ''),
            is_inventory_valuation_pending=data.get('is_inventory_valuation_pending', False),
            lock_details=data.get('lock_details', {}),
            exchange_rate=data.get('exchange_rate', 1.0),
            line_items=data.get('line_items', []),
            is_autobill_enabled=data.get('is_autobill_enabled', False),
            inprocess_transaction_present=data.get('inprocess_transaction_present', False),
            allow_partial_payments=data.get('allow_partial_payments', False),
            price_precision=data.get('price_precision', 2),
            sub_total=data.get('sub_total', 0.0),
            tax_total=data.get('tax_total', 0.0),
            discount_total=data.get('discount_total', 0.0),
            discount_percent=data.get('discount_percent', 0.0),
            discount=data.get('discount', 0.0),
            discount_applied_on_amount=data.get('discount_applied_on_amount', 0.0),
            discount_type=data.get('discount_type', ''),
            tax_override_preference=data.get('tax_override_preference', ''),
            is_discount_before_tax=data.get('is_discount_before_tax', True),
            adjustment=data.get('adjustment', 0.0),
            adjustment_description=data.get('adjustment_description', ''),
            shipping_charge_tax_id=data.get('shipping_charge_tax_id', ''),
            shipping_charge_tax_name=data.get('shipping_charge_tax_name', ''),
            shipping_charge_tax_type=data.get('shipping_charge_tax_type', ''),
            shipping_charge_tax_percentage=data.get('shipping_charge_tax_percentage', ''),
            shipping_charge_tax_exemption_id=data.get('shipping_charge_tax_exemption_id', ''),
            shipping_charge_tax_exemption_code=data.get('shipping_charge_tax_exemption_code', ''),
            shipping_charge_tax=data.get('shipping_charge_tax', ''),
            bcy_shipping_charge_tax=data.get('bcy_shipping_charge_tax', ''),
            shipping_charge_exclusive_of_tax=data.get('shipping_charge_exclusive_of_tax', 0.0),
            shipping_charge_inclusive_of_tax=data.get('shipping_charge_inclusive_of_tax', 0.0),
            shipping_charge_tax_formatted=data.get('shipping_charge_tax_formatted', ''),
            shipping_charge_exclusive_of_tax_formatted=data.get('shipping_charge_exclusive_of_tax_formatted', ''),
            shipping_charge_inclusive_of_tax_formatted=data.get('shipping_charge_inclusive_of_tax_formatted', ''),
            shipping_charge=data.get('shipping_charge', 0.0),
            bcy_shipping_charge=data.get('bcy_shipping_charge', 0.0),
            bcy_adjustment=data.get('bcy_adjustment', 0.0),
            bcy_sub_total=data.get('bcy_sub_total', 0.0),
            bcy_discount_total=data.get('bcy_discount_total', 0.0),
            bcy_tax_total=data.get('bcy_tax_total', 0.0),
            bcy_total=data.get('bcy_total', 0.0),
            total=data.get('total', 0.0),
            balance=data.get('balance', 0.0),
            write_off_amount=data.get('write_off_amount', 0.0),
            roundoff_value=data.get('roundoff_value', 0.0),
            transaction_rounding_type=data.get('transaction_rounding_type', ''),
            is_inclusive_tax=data.get('is_inclusive_tax', False),
            sub_total_inclusive_of_tax=data.get('sub_total_inclusive_of_tax', 0.0),
            contact_category=data.get('contact_category', ''),
            tax_rounding=data.get('tax_rounding', ''),
            taxes=data.get('taxes', []),
            tds_calculation_type=data.get('tds_calculation_type', ''),
            can_send_invoice_sms=data.get('can_send_invoice_sms', True),
            payment_expected_date=parse_date(data.get('payment_expected_date')),
            stop_reminder_until_payment_expected_date=data.get('stop_reminder_until_payment_expected_date', False),
            last_payment_date=parse_date(data.get('last_payment_date')),
            ach_supported=data.get('ach_supported', False),
            ach_payment_initiated=data.get('ach_payment_initiated', False),
            payment_options=data.get('payment_options', {}),
            reader_offline_payment_initiated=data.get('reader_offline_payment_initiated', False),
            contact_persons=data.get('contact_persons', []),
            attachment_name=data.get('attachment_name', ''),
            documents=data.get('documents', []),
            computation_type=data.get('computation_type', ''),
            deliverychallans=data.get('deliverychallans', []),
            merchant_id=data.get('merchant_id', ''),
            merchant_name=data.get('merchant_name', ''),
            ecomm_operator_id=data.get('ecomm_operator_id', ''),
            ecomm_operator_name=data.get('ecomm_operator_name', ''),
            salesorder_id=data.get('salesorder_id', ''),
            salesorder_number=data.get('salesorder_number', ''),
            salesorders=data.get('salesorders', []),
            shipping_bills=data.get('shipping_bills', []),
            contact_persons_details=data.get('contact_persons_details', []),
            includes_package_tracking_info=data.get('includes_package_tracking_info', False),
            approvers_list=data.get('approvers_list', []),
            qr_code=data.get('qr_code', {}),
            created_time=parse_date(data.get('created_time')),
            last_modified_time=parse_date(data.get('last_modified_time')),
            created_date=parse_date(data.get('created_date')),
            created_by_id=data.get('created_by_id', ''),
            created_by_name=data.get('created_by_name', ''),
            last_modified_by_id=data.get('last_modified_by_id', ''),
            page_width=data.get('page_width', ''),
            page_height=data.get('page_height', ''),
            orientation=data.get('orientation', ''),
            is_backorder=data.get('is_backorder', ''),
            sales_channel=data.get('sales_channel', ''),
            color_code=data.get('color_code', ''),
            current_sub_status_id=data.get('current_sub_status_id', ''),
            current_sub_status=data.get('current_sub_status', ''),
            sub_statuses=data.get('sub_statuses', []),
            estimate_id=data.get('estimate_id', ''),
            is_client_review_settings_enabled=data.get('is_client_review_settings_enabled', False),
            unused_retainer_payments=data.get('unused_retainer_payments', 0.0),
            tax_amount_withheld=data.get('tax_amount_withheld', 0.0),
            schedule_time=data.get('schedule_time', ''),
            customer_default_billing_address=data.get('customer_default_billing_address', {}),
            subject_content=data.get('subject_content', ''),
            can_send_in_mail=data.get('can_send_in_mail', False),
            invoice_url=data.get('invoice_url', ''),
            notes=data.get('notes', ''),
            terms=data.get('terms', ''),
            billing_address=data.get('billing_address', {}),
            shipping_address=data.get('shipping_address', {}),
            contact=data.get('contact', {}),
            inserted_in_qb=data.get('inserted_in_qb', False)
        )
    except Exception as e:
        print(f"Error creating instance: {e}")
        return None
    return instance
    

def parse_date(datetime_str):
    if not datetime_str:
        return None
    try:
        # Parse the datetime string assuming it has a timezone
        aware_datetime = datetime.fromisoformat(datetime_str)
        # date = aware_datetime.date().strftime('%Y-%m-%d')
        date = aware_datetime.date()
        print(date)
        return date
    except ValueError:
        # If parsing fails, return None or handle it appropriately
        return None