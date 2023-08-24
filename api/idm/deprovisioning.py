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
import pprint
import time
import json
import hashlib
import hmac
import base64
import requests
from django.db import transaction
from config.settings.common import env
from api.models import User


class Deprovisioner:
    model = User
    REQUEST_OBJ_COUNT = 500
    identifier_field = "username"

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

        b64mac = base64.b64encode(
            hmac.new(
                self.SECRET_KEY, bytes(encoded_data, "utf-8"), hashlib.sha1
            ).digest()
        )
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
        queryset_partition = self.queryset[
            n * self.REQUEST_OBJ_COUNT: (n + 1) * self.REQUEST_OBJ_COUNT
        ]

        while queryset_partition:
            prepared_rpc_bodies = [
                self.prepare_obj_json_rpc(user_obj) for user_obj in queryset_partition
            ]
            self.request_bodies.append(json.dumps(prepared_rpc_bodies, sort_keys=True))
            n += 1
            queryset_partition = self.queryset[
                n * self.REQUEST_OBJ_COUNT: (n + 1) * self.REQUEST_OBJ_COUNT
            ]

    def prepare_obj_json_rpc(self, obj):
        """
        Prepare the object for a JSON-RPC request for one user.
        """
        body_obj = {
            "jsonrpc": "2.0",
            "method": "idm.read",
            "id": f"{getattr(obj, self.identifier_field)}",
            "params": {
                "object": ["shortstamm"],
                "filter": [f"db.hrzlogin={getattr(obj, self.identifier_field)} && db.accountstatus=L"],
                "datain": {"timestamp": self.time, "returns": None, "debug": False},
            },
        }
        return body_obj

    def deprovison(self):
        self.pre_deprovison()
        self.prepare_request_bodies()

        for body in self.request_bodies:
            mac = self.create_hmac(body)
            headers = self.create_headers(mac)
            response = requests.post(
                self.idm_api_url, data=body, headers=headers, verify=True
            )
            parsed_content = json.loads(response.content)
            self.handle_response(parsed_content)

    def pre_deprovison(self):
        self.delete_marked_objects()

    def delete_marked_objects(self):
        self.get_queryset().filter(marked_for_deletion=True).delete()

    def mark_for_deletion(self, response_body):
        with transaction.atomic():
            for body_obj in response_body:
                self.model.objects.filter(
                    **{self.identifier_field: body_obj["id"]}
                ).update(
                    marked_for_deletion=self.get_update_value(body_obj)
                )

    def handle_response(self, response_body):
        self.mark_for_deletion(response_body)

    def get_update_value(self, obj):
        assert isinstance(obj, dict)
        return obj["result"]["resultsize"] > 0
