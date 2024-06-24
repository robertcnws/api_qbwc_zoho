# project/urls.py
from django.urls import path
from . import views

app_name = 'api_zoho_invoices'

urlpatterns = [
    path("list_invoices/", views.list_invoices, name="list_invoices"),
]
