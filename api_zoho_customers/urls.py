# project/urls.py
from django.urls import path
from . import views

app_name = 'api_zoho_customers'

urlpatterns = [
    path("list_customers/", views.list_customers, name="list_customers"),
    path("load_customers/", views.load_customers, name="load_customers"),
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("view_customer/<customer_id>", views.view_customer, name="view_customer"),
]
