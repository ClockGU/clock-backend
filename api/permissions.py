import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class AccessOwnDataPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id
