from rest_framework import serializers


class FeedBackSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    title = serializers.CharField()
    message = serializers.CharField()
