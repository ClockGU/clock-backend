from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import index, ContractViewSet, ShiftViewSet

app_name = "api"
router = DefaultRouter()
router.register(r"contracts", ContractViewSet, base_name="contracts")
router.register(r"shifts", ShiftViewSet, base_name="shifts")

urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path("", include(router.urls)),
]
