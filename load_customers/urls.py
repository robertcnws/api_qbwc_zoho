# project/urls.py
from django.contrib import admin
from django.urls import path 
from . import views

app_name = 'load_customers'

urlpatterns = [
    path("upload/", views.upload_file, name="upload"),
    path("list_customers/", views.list_customers, name="list_customers"),
]
