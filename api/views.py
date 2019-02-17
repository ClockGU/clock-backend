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

    def add_user_id(self, serializer):
        user_id = self.request.user_id
        data = serializer.initial_data.dict()
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
        if request.method in ["POST", "PUT"]:
            seri.initial_data = self.add_user_id(seri)
            return seri

        if request.method == "PATCH":
            # Not allowed keys "user" and "created_by" in a PATCH-Request.
            # Set "modified_by" to the user issuing the request
            seri.initial_data.pop("user", None)
            seri.initial_data.pop("created_by", None)
            seri.initial_data["modified_by"] = request.user_id
            return seri

        return seri
