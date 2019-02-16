from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
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

    def add_user_id(self, request):
        user_id = request.user_id
        data = request.data.dict()
        data["user"] = user_id
        data["created_by"] = user_id
        data["modified_by"] = user_id
        return data

    def get_queryset(self):
        queryset = super(ContractViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user_id)

    def get_serializer(self, *args, **kwargs):
        seri = super(ContractViewSet, self).get_serializer(*args, **kwargs)
        request = self.request
        if request.method == "POST":
            seri.initial_data = self.add_user_id(request)
            return seri

        return seri
