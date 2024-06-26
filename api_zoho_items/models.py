from django.db import models

class ZohoItem(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    qb_list_id = models.CharField(max_length=50, blank=True)
    
    def save(self, *args, **kwargs):
        if not (
            ZohoItem.objects.filter(item_id=self.item_id).exists() or 
            ZohoItem.objects.filter(sku=self.sku).exists() or 
            ZohoItem.objects.filter(qb_list_id=self.qb_list_id).exists()
        ) and self.status == 'active':
            super(ZohoItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name