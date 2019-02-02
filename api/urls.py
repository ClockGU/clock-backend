from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from api.views import index


router = DefaultRouter()


urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path("", include(router.urls)),
]
