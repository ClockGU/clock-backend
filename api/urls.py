from django.urls import path
from django.conf.urls import url

from api.views import index

urlpatterns = [
    path('', index, name='index')

]
