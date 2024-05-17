import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, serializers, views
from rest_framework.views import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from api.permissions import IsSupervisorPermission
from api.serializers import UserSerializer
from .encryption import decrypt_token
from .models import AuthKey
from cryptography.fernet import InvalidToken
from json import JSONDecodeError


class VerifySerializer(serializers.Serializer):
    auth_key = serializers.CharField()


class VerifyEndpoint(generics.GenericAPIView):
    serializer_class = VerifySerializer

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
            raise serializers.ValidationError(
                "Invalid Data: The provided key can no longer be used for authentication.")
        if not (email == auth_key_instance.email == user.email):
            return Response(status=HTTP_401_UNAUTHORIZED)
        user.is_supervisor = True
        user.save()
        auth_key_instance.delete()
        return Response(data=UserSerializer(user).data)


class ReportingEndpoint(generics.GenericAPIView):
    permission_classes = (IsSupervisorPermission,)

    def get(self, request, month=None, year=None):
        # user_query = "&users=".join(request.user.object_references)
        # response = requests.get(url=f"{settings.TIME_VAULT_URL}/reports?month={month}&year={year}")
        data = [{'days_content':
            {
                '02.05.2024': {'started': '10:00', 'stopped': '14:00', 'break_time': '00:00', 'work_time': '04:00',
                               'absence_type': '', 'type': 'Schicht', 'notes': ''},
                '06.05.2024': {'started': '09:00', 'stopped': '12:00', 'break_time': '00:00', 'work_time': '03:00',
                               'absence_type': '', 'type': 'Schicht', 'notes': ''},
                '07.05.2024': {'started': '18:00', 'stopped': '22:00', 'break_time': '00:00', 'work_time': '04:00',
                               'absence_type': '', 'type': 'Schicht', 'notes': '4'},
                '12.05.2024': {'started': '10:00', 'stopped': '12:00', 'break_time': '00:00', 'work_time': '02:00',
                               'absence_type': '', 'type': 'Schicht', 'notes': '6'},
                '15.05.2024': {'started': '14:00', 'stopped': '18:00', 'break_time': '00:00', 'work_time': '04:00',
                               'absence_type': '', 'type': 'Schicht', 'notes': ''}
            },
            'general':
                {
                    'user_name': 'Grossmüller, Christian',
                    'personal_number': None,
                    'contract_name': '22',
                    'month': 5,
                    'year': 2024,
                    'long_month_name': 'Mai',
                    'debit_worktime': '22:00',
                    'total_worked_time': '17:00',
                    'last_month_carry_over': '00:00',
                    'next_month_carry_over': '-05:00',
                    'net_worktime': '17:00',
                }
        }]
        return Response(data=data)
