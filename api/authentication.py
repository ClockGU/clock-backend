# api/authentication.py
import jwt
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

User = get_user_model()

def _get_token(request):
    auth = get_authorization_header(request).decode()
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    cookie = getattr(settings, "JWT_AUTH_COOKIE", None)
    if cookie and cookie in request.COOKIES:
        return request.COOKIES[cookie]
    raise exceptions.AuthenticationFailed("Missing bearer token")

class ExternalJWTUser:
    def __init__(self, payload):
        sub = payload.get("sub")
        self.id = uuid.UUID(sub) if sub else None  
        self.username = payload.get("username")
        self.email = payload.get("email")
        self.first_name = payload.get("first_name")
        self.last_name = payload.get("last_name")
        self.user_role = payload.get("user_role")
        self.language = payload.get("language")
        self.dsgvo_accepted = payload.get("dsgvo_accepted")
        self.is_staff = payload.get("is_staff", False)
        self.is_active = payload.get("is_active", True)
        self.is_superuser = payload.get("is_superuser", False)
        self.personal_number = payload.get("personal_number")
        self.exp = payload.get("exp")

    @property
    def is_authenticated(self):
        return True

def user_info(payload):
    return ExternalJWTUser(payload)

class ExternalJWTAuthentication(BaseAuthentication):
    """Verify RS256 token from HR-Login"""
    def authenticate(self, request):
        #import remote_pdb; remote_pdb.set_trace('0.0.0.0',4444)
        token = _get_token(request)
        public_key_path = settings.JWT_PUBLIC_KEY
        with open(public_key_path, "r") as f:
            public_key = f.read()
        algorithm = getattr(settings, "JWT_ALGORITHM", "RS256")
        if not public_key:
            raise exceptions.AuthenticationFailed("Auth public key not configured")
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {e}")

        user = user_info(payload)
        return (user, token)
