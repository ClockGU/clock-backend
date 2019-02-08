import jwt
import os
from django.http import HttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from api.tasks import twenty_second_task, async_5_user_creation

from api.models import Contract

from api.serializers import ContractSerializer

# Proof of Concept that celery works


def index(request):
    async_5_user_creation.delay()
    return HttpResponse("A Dummy site.")


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    name = "contracts"

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def create(self, request, *args, **kwargs):
        jwt_token = request.META.get("header").split()[-1]
        user_id = jwt.decode(
            jwt_token, os.environ.get("DJANGO_SECRET_KEY"), algorithm="HS256"
        )["user_id"]

        data = request.data.dict()
        data["user"] = user_id
        data["created_by"] = user_id
        data["modified_by"] = user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
