from django.urls import path
from . import views

app_name = 'api_quickbook_soap'

urlpatterns = [
    path("customer_query/", views.customer_query, name="customer_query"),
]