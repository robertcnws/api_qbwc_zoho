from django.urls import path
from . import views

app_name = 'api_quickbook_soap'

urlpatterns = [
    path("quickbook_api_settings/", views.quickbook_api_settings, name="quickbook_api_settings"),
    path("customer_query/", views.customer_query, name="customer_query"),
    path("item_query/", views.item_query, name="item_query"),
    path("matching_items/", views.matching_items, name="matching_items"),
    path("matching_customers/", views.matching_customers, name="matching_customers"),
    path("match_all_first_items_ajax/", views.match_all_first_items_ajax, name="match_all_first_items_ajax"),
    path("match_all_first_customers_ajax/", views.match_all_first_customers_ajax, name="match_all_first_customers_ajax"),
    path("match_one_item_ajax/", views.match_one_item_ajax, name="match_one_item_ajax"),
    path("match_one_customer_ajax/", views.match_one_customer_ajax, name="match_one_customer_ajax"),
    path("matched_items/", views.matched_items, name="matched_items"),
    path("matched_customers/", views.matched_customers, name="matched_customers"),
]