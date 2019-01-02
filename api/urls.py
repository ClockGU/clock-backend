from django.urls import path
from django.conf.urls import url

from api.views import index

urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index")
]
