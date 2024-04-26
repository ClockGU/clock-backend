"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
from uuid import uuid4

import requests
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .provider import GoetheUniProvider


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


class ProviderAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        adapter = GoetheUniOAuth2Adapter(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)

        redirect_uri = request.GET.get("redirect_uri")
        if redirect_uri not in settings.GOETHE_OAUTH2_REDIRECT_URIS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        authorize_url = adapter.authorize_url
        state = str(uuid4())

        data = {
            "authorization_url": f"{authorize_url}?response_type=code&client_id={app.client_id}&redirect_uri={redirect_uri}&state={state}&scope=user"
        }

        return Response(data)


class GoetheUniLogin(SocialLoginView):
    adapter_class = GoetheUniOAuth2Adapter
    client_class = OAuth2Client


oauth2_login = OAuth2LoginView.adapter_view(GoetheUniOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GoetheUniOAuth2Adapter)
