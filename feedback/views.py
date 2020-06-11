from rest_framework import generics
from rest_framework.response import Response
from feedback.serializers import FeedBackSerializer
from django.core.mail import EmailMessage
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
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
            to=[settings.SYSTEM_EMAILS["RECEIVER"]],
            reply_to=[data["email"], settings.SYSTEM_EMAILS["RECEIVER"]],
        )
        message.send(fail_silently=False)

        if not message:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data)
