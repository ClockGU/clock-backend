from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Faq
from .serializers import FaqSerializer

# Create your views here.


class FaqViewSet(ReadOnlyModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    name = "faqs"
