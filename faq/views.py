from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from .models import Faq
from .serializers import FaqSerializer

# Create your views here.


class FaqViewSet(ReadOnlyModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    name = "faqs"
    permission_classes = [AllowAny]
