# project/urls.py
from django.urls import path
from . import views

app_name = 'api_zoho_customers'

urlpatterns = [
    path("list_customers/", views.list_customers, name="list_customers"),
]
