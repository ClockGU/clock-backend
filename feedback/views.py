from django.conf import settings
from django.core.mail import EmailMessage
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from feedback.serializers import FeedBackSerializer

from .utils import format_message


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

        receiver = settings.SYSTEM_EMAILS["RECEIVER"]
        if data["title"] == "Ombud":
            receiver = settings.SYSTEM_EMAILS["RECEIVER_OMBUD"]

        message = EmailMessage(
            subject=data["title"],
            body=format_message(
                request.build_absolute_uri(),
                data["name"],
                data["email"],
                data["message"],
            ),
            from_email="Clock Feedback <{email}>".format(
                name=data["name"], email=settings.SYSTEM_EMAILS["SENDER"]
            ),
            to=[receiver],
            cc=[data["email"]],
            reply_to=[data["email"], settings.SYSTEM_EMAILS["RECEIVER"]],
        )
        message.send(fail_silently=False)

        if not message:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data)
