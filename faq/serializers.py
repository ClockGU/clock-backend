from rest_framework.serializers import ModelSerializer

from .models import Faq


class FaqSerializer(ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"
