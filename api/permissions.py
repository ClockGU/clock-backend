import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class AccessOwnDataPermission(IsAuthenticated):
    """
    Permission class which only permits access of Objects which are owned by the
    User issueing the request.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id
