"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
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
