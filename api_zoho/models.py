from django.db import models

# Create your models here.
class AppConfig(models.Model):
    app_id = models.AutoField(primary_key=True)
    # Zoho API connection fields
    zoho_client_id = models.CharField(max_length=255, blank=True, null=True)
    zoho_client_secret = models.CharField(max_length=255, blank=True, null=True)
    zoho_org_id = models.CharField(max_length=255, blank=True, null=True)
    zoho_redirect_uri = models.CharField(max_length=255, blank=True, null=True)
    zoho_refresh_time = models.DurationField(blank=True, null=True)
    zoho_refresh_token = models.CharField(max_length=255, blank=True, null=True)
    zoho_access_token = models.CharField(max_length=255, blank=True, null=True)
    zoho_connection_configured = models.BooleanField(default=False)
    qb_username = models.CharField(max_length=255, blank=True, null=True)
    qb_password = models.CharField(max_length=255, blank=True, null=True)
    qb_owner_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and AppConfig.objects.exists():
            # Update the existing instance if there is one
            self.pk = AppConfig.objects.get().pk

        # Check if all required fields for Zoho connection are present
        required_fields = [
            self.zoho_client_id,
            self.zoho_client_secret,
            self.zoho_org_id,
            self.zoho_redirect_uri,
        ]

        # Set zoho_connection_configured to True if all fields are not empty, else False
        self.zoho_connection_configured = all(field is not None and field != "" for field in required_fields)

        super(AppConfig, self).save(*args, **kwargs)

    def __str__(self):
        return "App Configuration"