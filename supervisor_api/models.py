import base64
import json
import logging
import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models

from supervisor_api.mail import format_message

from .encryption import encrypt_data, fernet

LOGGER = logging.getLogger("supervisor")


class AuthKey(models.Model):
    key = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.id is None:
            data = {"key": str(self.key), "email": self.email}
            token = encrypt_data(json.dumps(data))
            message = format_message(token)

            message = EmailMessage(
                subject="Zugangsdaten Clock für Vorgesetzte",
                body=message,
                from_email="Clock <{email}>".format(
                    email=settings.SYSTEM_EMAILS["SENDER"]
                ),
                to=[self.email],
            )
            message.send(fail_silently=False)
            LOGGER.info(token)
        super(AuthKey, self).save(force_insert, force_update, using, update_fields)
