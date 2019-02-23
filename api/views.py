from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from api.tasks import async_5_user_creation

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

    def get_queryset(self):
        queryset = super(ContractViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user.id)
