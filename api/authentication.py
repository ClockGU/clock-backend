# api/authentication.py
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
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

def user_info(claims):
    return {
        "sub": claims["sub"],
        "email": claims.get("email", ""),
        "first_name": claims.get("first_name", ""),
        "last_name": claims.get("last_name", ""),
    }

class ExternalJWTAuthentication(BaseAuthentication):
    """Verify RS256 token from HR-Login"""
    def authenticate(self, request):
        #import remote_pdb; remote_pdb.set_trace('0.0.0.0',4444)  
        token = _get_token(request)
        pubkey = settings.JWT_PUBLIC_KEY
        if not pubkey:
            raise exceptions.AuthenticationFailed("Auth public key not configured")
        try:
            user_data = jwt.decode(
                token,
                pubkey,
                algorithms=["RS256"],
                issuer=getattr(settings, "AUTH_ISSUER", None),
                audience=getattr(settings, "AUTH_AUDIENCE", None),
                options={"require": ["exp", "sub"]},
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {e}")

        user = user_info(user_data)
        return (user, token)
