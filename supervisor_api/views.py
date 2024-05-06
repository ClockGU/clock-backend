from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.views import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from api.serializers import DjoserUserSerializer
from .encryption import decrypt_token
from .models import AuthKey
from cryptography.fernet import InvalidToken
from json import JSONDecodeError

class VerifySerializer(serializers.Serializer):
    auth_key = serializers.CharField()


class VerifyEndpoint(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        decrypted_data = {}
        try:
            decrypted_data = decrypt_token(data["auth_key"])
        except (InvalidToken, JSONDecodeError) as error:
            if isinstance(error, InvalidToken):
                raise serializers.ValidationError("Invalid key: Key was not generated by the System.")
            if isinstance(error, JSONDecodeError):
                raise serializers.ValidationError("Invalid key: Decrypted data is not JSON serializable.")
        try:
            key = decrypted_data["key"]
            email = decrypted_data["email"]
        except KeyError:
            raise serializers.ValidationError("Invalid Data: Decrypted data does not contain necessary information.")

        try:
            auth_key_instance = AuthKey.objects.get(key=key)
        except AuthKey.DoesNotExist:
            raise serializers.ValidationError("Invalid Data: The provided key can no longer be used for authentication.")
        if not (email == auth_key_instance.email == user.email):
            return Response(status=HTTP_401_UNAUTHORIZED)
        user.is_supervisor = True
        user.save()
        auth_key_instance.delete()
        return Response(data=DjoserUserSerializer(user).data)
