from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from api.views import index, ContractViewSet


router = DefaultRouter()
router.register(r"contracts", ContractViewSet)

urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path("", include(router.urls)),
]
