from django.shortcuts import redirect, render
from django.conf import settings
from django.http import JsonResponse
import requests
import os
from django.urls import reverse
from django.contrib import messages
from .models import AppConfig
from .forms import ApiZohoForm


def generate_auth_url(request):
    app_config = AppConfig.objects.first()
    client_id = app_config.zoho_client_id
    redirect_uri = app_config.zoho_redirect_uri
    scopes = settings.ZOHO_SCOPE_INVOICES + ',' + settings.ZOHO_SCOPE_ITEMS + ',' + settings.ZOHO_SCOPE_CUSTOMERS
    auth_url = f"https://accounts.zoho.com/oauth/v2/auth?scope={scopes}&client_id={client_id}&response_type=code&access_type=offline&redirect_uri={redirect_uri}"
    return redirect(auth_url)


def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
    else:
        raise Exception("Error retrieving access token")

    return access_token


def get_refresh_token(request):
    authorization_code = request.GET.get("code", None)
    if not authorization_code:
        messages.error(request, "Authorization code is missing")
        return redirect(reverse("api_zoho:zoho_api_connect"))
    app_config = AppConfig.objects.first()
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "code": authorization_code,
        "client_id": app_config.zoho_client_id,
        "client_secret": app_config.zoho_client_secret,
        "redirect_uri": app_config.zoho_redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    response_json = response.json()
    access_token = response_json.get("access_token", None)
    refresh_token = response_json.get("refresh_token", None)

    if access_token and refresh_token:
        app_config = AppConfig.objects.first()
        if app_config:
            app_config.zoho_refresh_token = refresh_token
            app_config.save()
        return redirect(reverse("api_zoho:zoho_api_connect"))
    else:
        messages.error(
            request,
            "Failed to obtain access_token and/or refresh_token: {}".format(
                response_json
            ),
        )
        return redirect(reverse("api_zoho:zoho_api_connect"))


# GET THE ZOHO API ACCESS TOKEN
def zoho_api_settings(request):
    app_config = AppConfig.objects.first()
    if not app_config:
        app_config = AppConfig.objects.create()
    zoho_connection_configured = app_config.zoho_connection_configured
    connected = (
        app_config.zoho_connection_configured
        and app_config.zoho_refresh_token is not None
        or ""
    )
    if request.method == "GET":
        form = ApiZohoForm(instance=app_config)
    elif request.method == "POST":
        form = ApiZohoForm(request.POST, instance=app_config)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Zoho API settings have been updated successfully."
            )
            return redirect("zoho_api:zoho_api_settings")
        else:
            messages.error(
                request,
                "There was an error updating Zoho API settings. Please correct the errors below.",
            )
    auth_url = None
    if not connected:
        auth_url = reverse("api_zoho:generate_auth_url")
    context = {
        "connected": connected,
        "auth_url": auth_url,
        "zoho_connection_configured": app_config.zoho_connection_configured,
        "active_page": "settings",
    }
    return render(request, "api_zoho/zoho_api_settings.html", context)


def zoho_api_connect(request):
    app_config = AppConfig.objects.first()
    if app_config.zoho_connection_configured:
        try:
            access_token = get_access_token(
                app_config.zoho_client_id,
                app_config.zoho_client_secret,
                app_config.zoho_refresh_token,
            )
            messages.success(request, "Zoho API connected successfully.")
        except Exception as e:
            messages.error(request, f"Error connecting to Zoho API: {str(e)}")
    else:
        messages.warning(request, "Zoho API connection is not configured yet.")
    return redirect("api_zoho:zoho_api_settings")


def config_headers(request):
    app_config = AppConfig.objects.first()
    access_token = app_config.zoho_access_token
    if not access_token:
        access_token = get_access_token(
            app_config.zoho_client_id,
            app_config.zoho_client_secret,
            app_config.zoho_refresh_token,
        )
        app_config.zoho_access_token = access_token
        app_config.save()
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    return headers


def home(request):
    return render(request, 'api_zoho/home.html')    