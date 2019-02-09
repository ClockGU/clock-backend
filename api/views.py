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

    def get_queryset(self):
        queryset = super(ContractViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user_id)

    def create(self, request, *args, **kwargs):
        user_id = request.user_id
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
