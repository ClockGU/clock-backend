from rest_framework import serializers


class FeedBackSerializer(serializers.Serializer):

    username = serializers.CharField()
    userEmail = serializers.EmailField()
    emailTitle = serializers.CharField()
    emailContent = serializers.CharField()
