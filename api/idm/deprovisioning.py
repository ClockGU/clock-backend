import timeit
import time
import json
import hashlib
import hmac
import base64
import requests
from config.settings.common import env
from api.models import User


class Deprovisioner:
    model = User

    def __init__(self, user_queryset=None):
        self.idm_api_url = env.str("IDM_API_URL")
        self.API_KEY = env.str("IDM_API_KEY")
        self.SECRET_KEY = bytes.fromhex(env.str("IDM_SECRET_KEY"))
        self.queryset = user_queryset if user_queryset else self.get_queryset()
        self.request_bodies = []

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.model.objects.all()
