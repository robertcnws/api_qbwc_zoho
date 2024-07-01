from django.db import models

class ZohoFullInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_id = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    date = models.DateField(blank=True)
    due_date = models.DateField(blank=True)
    offline_created_date_with_time = models.CharField(max_length=100, blank=True)
    customer_id = models.CharField(max_length=100, blank=True)
    customer_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    currency_id = models.CharField(max_length=100, blank=True)
    invoice_source = models.CharField(max_length=50, blank=True)
    currency_code = models.CharField(max_length=10, blank=True)
    currency_symbol = models.CharField(max_length=10, blank=True)
    currency_name_formatted = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, blank=True)
    recurring_invoice_id = models.CharField(max_length=100, blank=True)
    payment_terms = models.IntegerField(default=0, blank=True)
    payment_terms_label = models.CharField(max_length=100, blank=True)
    payment_reminder_enabled = models.BooleanField(default=False)
    payment_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    credits_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    payment_made = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    zcrm_potential_id = models.CharField(max_length=100, blank=True)
    zcrm_potential_name = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    is_inventory_valuation_pending = models.BooleanField(default=False)
    lock_details = models.JSONField(default=dict, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, blank=True)
    line_items = models.JSONField(default=list, blank=True)
    is_autobill_enabled = models.BooleanField(default=False)
    inprocess_transaction_present = models.BooleanField(default=False)
    allow_partial_payments = models.BooleanField(default=False)
    price_precision = models.IntegerField(default=2, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    discount_applied_on_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    discount_type = models.CharField(max_length=50, blank=True)
    tax_override_preference = models.CharField(max_length=50, blank=True)
    is_discount_before_tax = models.BooleanField(default=True)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    adjustment_description = models.CharField(max_length=255, blank=True)
    shipping_charge_tax_id = models.CharField(max_length=100, blank=True)
    shipping_charge_tax_name = models.CharField(max_length=100, blank=True)
    shipping_charge_tax_type = models.CharField(max_length=50, blank=True)
    shipping_charge_tax_percentage = models.CharField(max_length=50, blank=True)
    shipping_charge_tax_exemption_id = models.CharField(max_length=100, blank=True)
    shipping_charge_tax_exemption_code = models.CharField(max_length=100, blank=True)
    shipping_charge_tax = models.CharField(max_length=50, blank=True)
    bcy_shipping_charge_tax = models.CharField(max_length=50, blank=True)
    shipping_charge_exclusive_of_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    shipping_charge_inclusive_of_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    shipping_charge_tax_formatted = models.CharField(max_length=100, blank=True)
    shipping_charge_exclusive_of_tax_formatted = models.CharField(max_length=100, blank=True)
    shipping_charge_inclusive_of_tax_formatted = models.CharField(max_length=100, blank=True)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    bcy_shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    bcy_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    bcy_sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bcy_discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    bcy_tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    bcy_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    write_off_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    roundoff_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    transaction_rounding_type = models.CharField(max_length=50, blank=True)
    is_inclusive_tax = models.BooleanField(default=False)
    sub_total_inclusive_of_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    contact_category = models.CharField(max_length=50, blank=True)
    tax_rounding = models.CharField(max_length=50, blank=True)
    taxes = models.JSONField(default=list, blank=True)
    tds_calculation_type = models.CharField(max_length=50, blank=True)
    can_send_invoice_sms = models.BooleanField(default=True)
    payment_expected_date = models.DateField(blank=True, null=True)
    stop_reminder_until_payment_expected_date = models.BooleanField(default=False)
    last_payment_date = models.DateField(blank=True, null=True)
    ach_supported = models.BooleanField(default=False)
    ach_payment_initiated = models.BooleanField(default=False)
    payment_options = models.JSONField(default=dict, blank=True)
    reader_offline_payment_initiated = models.BooleanField(default=False)
    contact_persons = models.JSONField(default=list, blank=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    documents = models.JSONField(default=list, blank=True)
    computation_type = models.CharField(max_length=50, blank=True)
    deliverychallans = models.JSONField(default=list, blank=True)
    merchant_id = models.CharField(max_length=100, blank=True)
    merchant_name = models.CharField(max_length=255, blank=True)
    ecomm_operator_id = models.CharField(max_length=100, blank=True)
    ecomm_operator_name = models.CharField(max_length=255, blank=True)
    salesorder_id = models.CharField(max_length=100, blank=True)
    salesorder_number = models.CharField(max_length=50, blank=True)
    salesorders = models.JSONField(default=list, blank=True)
    shipping_bills = models.JSONField(default=list, blank=True)
    contact_persons_details = models.JSONField(default=list, blank=True)
    includes_package_tracking_info = models.BooleanField(default=False)
    approvers_list = models.JSONField(default=list, blank=True)
    qr_code = models.JSONField(default=dict, blank=True)
    created_time = models.DateTimeField(blank=True)
    last_modified_time = models.DateTimeField(blank=True)
    created_date = models.DateField(blank=True)
    created_by_id = models.CharField(max_length=100, blank=True)
    created_by_name = models.CharField(max_length=255, blank=True)
    last_modified_by_id = models.CharField(max_length=100, blank=True)
    page_width = models.CharField(max_length=50, blank=True)
    page_height = models.CharField(max_length=50, blank=True)
    orientation = models.CharField(max_length=50, blank=True)
    is_backorder = models.CharField(max_length=50, blank=True)
    sales_channel = models.CharField(max_length=100, blank=True)
    color_code = models.CharField(max_length=50, blank=True)
    current_sub_status_id = models.CharField(max_length=100, blank=True)
    current_sub_status = models.CharField(max_length=50, blank=True)
    sub_statuses = models.JSONField(default=list, blank=True)
    estimate_id = models.CharField(max_length=100, blank=True)
    is_client_review_settings_enabled = models.BooleanField(default=False)
    unused_retainer_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    tax_amount_withheld = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    schedule_time = models.CharField(max_length=50, blank=True)
    customer_default_billing_address = models.JSONField(default=dict, blank=True)
    subject_content = models.TextField(blank=True)
    can_send_in_mail = models.BooleanField(default=False)
    invoice_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)
    billing_address = models.JSONField(default=dict, blank=True)
    shipping_address = models.JSONField(default=dict, blank=True)
    contact = models.JSONField(default=dict, blank=True)
    inserted_in_qb = models.BooleanField(default=False, blank=True)
    items_unmatched = models.JSONField(default=list, blank=True)
    customer_unmatched = models.JSONField(default=list, blank=True)
    

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Si el objeto ya existe (tiene una clave primaria)
            # Permitir la actualización sin restricciones adicionales
            super(ZohoFullInvoice, self).save(*args, **kwargs)
        else:
            # if not (ZohoInvoice.objects.filter(invoice_id=self.invoice_id).exists() or ZohoInvoice.objects.filter(invoice_number=self.invoice_number).exists()) and self.status == 'active':
            if not (
                ZohoFullInvoice.objects.filter(invoice_id=self.invoice_id).exists() or ZohoFullInvoice.objects.filter(invoice_number=self.invoice_number).exists()
                ):
                super(ZohoFullInvoice, self).save(*args, **kwargs)
            else:   
                print(f"ZohoFullInvoice {self.invoice_id} ({self.invoice_number}) no guardado porque ya existe un objeto con el mismo invoice_id")

    class Meta:
        verbose_name = "Zoho Full Invoice"
        verbose_name_plural = "Zoho Full Invoices"

