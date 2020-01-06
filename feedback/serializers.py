from rest_framework import serializers


class FeedBackSerializer(serializers.Serializer):

    user_name = serializers.CharField()
    user_email = serializers.EmailField()
    email_title = serializers.CharField()
    email_content = serializers.CharField()
