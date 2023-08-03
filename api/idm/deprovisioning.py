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
    REQUEST_OBJ_COUNT = 500

    def __init__(self, user_queryset=None):
        self.idm_api_url = env.str("IDM_API_URL")
        self.API_KEY = env.str("IDM_API_KEY")
        self.SECRET_KEY = bytes.fromhex(env.str("IDM_SECRET_KEY"))
        self.queryset = user_queryset if user_queryset else self.get_queryset()
        self.request_bodies = []
        self.time = int(time.time() * 1000)

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.model.objects.all()

    def create_hmac(self, request_body):
        encoded_data = self.idm_api_url + request_body + self.API_KEY + str(self.time)

        b64mac = base64.b64encode(hmac.new(self.SECRET_KEY, bytes(encoded_data, "utf-8"), hashlib.sha1).digest())
        return b64mac

    def create_headers(self, b64mac):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-uniffm-apikey": self.API_KEY,
            "x-uniffm-time": str(self.time),
            "x-uniffm-mac": b64mac,
        }

    def prepare_request_bodies(self):
        """
        Prepare an Array of Strings each representing one Batch-Request body for an JSON-RPC Request.
        """
        assert len(self.request_bodies) == 0
        n = 0
        queryset_partition = self.queryset[n * self.REQUEST_OBJ_COUNT:(n + 1) * self.REQUEST_OBJ_COUNT]

        while queryset_partition:
            prepared_rpc_bodies = map(self.prepare_obj_json_rpc, queryset_partition)
            self.request_bodies.append(json.dumps(prepared_rpc_bodies, sort_keys=True))
            n += 1
            queryset_partition = self.queryset[n * self.REQUEST_OBJ_COUNT:(n + 1) * self.REQUEST_OBJ_COUNT]

    def prepare_obj_json_rpc(self, obj):
        """
        Prepare the object for a JSON-RPC request for one user.
        """
        body_obj = {
            "jsonrpc": "2.0",
            "method": "idm.read",
            "id": f"{obj.username}",
            "params": {
                "object": ["account"],
                "filter": [f"db.login={obj.username} && db.accountstatus=L"],
                "datain": {
                    "timestamp": self.time,
                    "returns": None,
                    "debug": False
                }
            }
        }
        return body_obj
