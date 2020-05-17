from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from uuid import uuid4

import logging

logger = logging.Logger(__name__)


class ProviderAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        adapter = GitHubOAuth2Adapter(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)

        redirect_uri = request.GET.get("redirect_uri")
        if redirect_uri != "http://localhost:8080/login":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        authorize_url = adapter.authorize_url
        state = str(uuid4())

        data = {
            "authorization_url": f"{authorize_url}?client_id={app.client_id}&redirect_uri={redirect_uri}&state={state}&scope=user"
        }

        return Response(data)


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8080/login"
    client_class = OAuth2Client
