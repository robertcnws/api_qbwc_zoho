from django.db import models

class ZohoItem(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    source = models.CharField(max_length=20)
    is_linked_with_zohocrm = models.BooleanField(default=False)
    zcrm_product_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    tax_name = models.CharField(max_length=50, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    purchase_account_id = models.CharField(max_length=50)
    purchase_account_name = models.CharField(max_length=255)
    account_id = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    purchase_description = models.TextField()
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2)
    item_type = models.CharField(max_length=20)
    product_type = models.CharField(max_length=20)
    stock_on_hand = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    has_attachment = models.BooleanField(default=False)
    available_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    actual_available_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sku = models.CharField(max_length=50)
    reorder_level = models.CharField(max_length=50, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_type = models.CharField(max_length=50, blank=True, null=True)
    image_document_id = models.CharField(max_length=50, blank=True, null=True)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    cf_qb_ref_id = models.CharField(max_length=50)
    cf_qb_ref_id_unformatted = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not (ZohoItem.objects.filter(item_id=self.item_id).exists() or ZohoItem.objects.filter(sku=self.sku).exists()) and self.status == 'active':
            super(ZohoItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name