from django import forms
from .models import AppConfig

class ApiZohoForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = ['zoho_client_id', 'zoho_client_secret','zoho_redirect_uri', 'zoho_org_id']