import base64
import json

from cryptography.fernet import Fernet
from django.conf import settings

SECRET_BYTES = bytes(settings.SECRET_KEY, "utf-8")

fernet = Fernet(base64.urlsafe_b64encode(SECRET_BYTES[:32]))


def encrypt_data(data):
    if not isinstance(data, str):
        raise TypeError("Data provided for encryption is not of type String.")

    return str(fernet.encrypt(bytes(data, "utf-8")), "utf-8")


def decrypt_token(token):
    return json.loads(fernet.decrypt(token))
