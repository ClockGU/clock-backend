from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from uuid import uuid4

import requests

from allauth.socialaccount import app_settings
from .provider import GoetheUniProvider


import logging

logger = logging.Logger(__name__)


class GoetheUniOAuth2Adapter(OAuth2Adapter):
    provider_id = GoetheUniProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})

    web_url = "https://cas.rz.uni-frankfurt.de/cas/oauth2.0"
    api_url = "https://cas.rz.uni-frankfurt.de/cas/oauth2.0"

    access_token_url = "{0}/accessToken".format(web_url)
    authorize_url = "{0}/authorize".format(web_url)
    profile_url = "{0}/profile".format(api_url)

    def complete_login(self, request, app, token, **kwargs):
        params = {"access_token": token.token}
        resp = requests.get(self.profile_url, params=params)
        resp.raise_for_status()
        extra_data = resp.json()
        attributes = extra_data["attributes"]
        extra_data["username"] = attributes["uid"]
        extra_data["email"] = attributes["mailPrimaryAddress"]
        extra_data["first_name"] = attributes["givenName"]
        extra_data["last_name"] = attributes["sn"]
        return self.get_provider().sociallogin_from_response(request, extra_data)

    # def get_email(self, token):
    #     email = None
    #     params = {"access_token": token.token}
    #     resp = requests.get(self.profile_url, params=params)
    #     resp.raise_for_status()
    #     json = resp.json()
    #     if resp.status_code == 200 and json:
    #         email = json["attributes"]["mailPrimaryAddress"]
    #     return email


class ProviderAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        adapter = GoetheUniOAuth2Adapter(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)

        redirect_uri = request.GET.get("redirect_uri")
        # if redirect_uri != adapter.get_callback_url(request, app):
        if redirect_uri != "https://clock.uni-frankfurt.de/login":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        authorize_url = adapter.authorize_url
        state = str(uuid4())

        data = {
            "authorization_url": f"{authorize_url}?response_type=code&client_id={app.client_id}&redirect_uri={redirect_uri}&state={state}&scope=user"
        }

        return Response(data)


class GoetheUniLogin(SocialLoginView):
    adapter_class = GoetheUniOAuth2Adapter
    callback_url = "https://clock.uni-frankfurt.de/login"
    client_class = OAuth2Client


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8080/login"
    client_class = OAuth2Client


oauth2_login = OAuth2LoginView.adapter_view(GoetheUniOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GoetheUniOAuth2Adapter)
