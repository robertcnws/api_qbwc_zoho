from django.db import models

class QbItem(models.Model):
    id = models.AutoField(primary_key=True)
    list_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    
    
    def save(self, *args, **kwargs):
        if not (QbItem.objects.filter(list_id=self.list_id).exists() or QbItem.objects.filter(name=self.name).exists()):
            super(QbItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
