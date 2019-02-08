import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class AccessOwnDataPermission(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super(AccessOwnDataPermission, self).has_permission(
            request, view
        )

        if is_authenticated:
            jwt_token = request.META.get("HTTP_AUTHORIZATION").split()[-1]
            user_id = jwt.decode(jwt_token, settings.SECRET_KEY, algorithm="HS256")[
                "user_id"
            ]
            request.user_id = user_id

        return is_authenticated

    def has_object_permission(self, request, view, obj):

        return request.user_id == obj.user.id
