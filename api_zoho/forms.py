from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AppConfig

class ApiZohoForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = ['zoho_client_id', 'zoho_client_secret','zoho_redirect_uri', 'zoho_org_id']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
