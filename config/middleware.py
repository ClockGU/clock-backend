from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs
from django.conf import settings
from jwt import decode as jwt_decode
from django.contrib.auth import get_user_model
from channels.exceptions import DenyConnection
#from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        '''
        Middleware to authenticate users using JWT tokens
        '''
        from django.contrib.auth.models import AnonymousUser
        headers = dict(scope["headers"])
        token = None
        if b"jwt_token" in headers:
            token = headers[b"jwt_token"]
            auth_header = token.decode()

        if not token:
            user = AnonymousUser()
        else:
            scope["user"] = None
            scope["is_authenticated"] = False
            User = get_user_model()
            try:
                decoded_data = jwt_decode(
                    token.decode(),
                    settings.SIMPLE_JWT["SIGNING_KEY"],
                    algorithms=[settings.SIMPLE_JWT["ALGORITHM"]]
                )
                user_id = decoded_data.get("user_id")
                user = await User.objects.aget(id=user_id)  
                scope["user"] = user  
                scope["is_authenticated"] = True

            except:
                scope["user"] = AnonymousUser()

        # Pass the request to the next middleware/application
        return await super().__call__(scope, receive, send)