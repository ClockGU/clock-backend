from rest_framework import generics
from rest_framework.response import Response
from feedback.serializers import FeedBackSerializer
from django.core.mail import send_mail
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from config.settings.common import env
from django.conf import settings


class FeedBackView(generics.GenericAPIView):
    serializer_class = FeedBackSerializer

    permission_classes = ()

    @swagger_auto_schema(
        responses={200: "The view responds with 200 after sending the email."}
    )
    def post(self, request, *args, **kwargs):
        serializer = FeedBackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        message = send_mail(
            subject=data["title"],
            from_email="{name} <{email}>".format(
                name=data["name"], email=data["email"]
            ),
            message=data["message"],
            recipient_list=[settings.SYSTEM_EMAIL],
            fail_silently=False,
        )
        if not message:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.data)
