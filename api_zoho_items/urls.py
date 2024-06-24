# project/urls.py
from django.urls import path
from . import views

app_name = 'api_zoho_items'

urlpatterns = [
    path("list_items/", views.list_items, name="list_items"),
]
