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
import base64
import datetime
import hashlib
import hmac
import json
import logging
import time

import requests
from dateutil.relativedelta import relativedelta
from django.db import transaction

from api.models import User
from config.settings.common import env

LOGGER = logging.getLogger("deprovisioning")


class Deprovisioner:
    model = User
    REQUEST_OBJ_COUNT = 500
    identifier_field = "username"
    deprovision_cond_field = "marked_for_deletion"

    def __init__(self, user_queryset=None):
        self.idm_api_url = env.str("IDM_API_URL")
        self.API_KEY = env.str("IDM_API_KEY")
        self.SECRET_KEY = bytes.fromhex(env.str("IDM_SECRET_KEY"))
        self.queryset = user_queryset if user_queryset else self.get_queryset()
        self.request_bodies = []
        self.last_deprovision_time = (
            datetime.datetime.now() - relativedelta(months=1)
        ).timestamp() * 1000
        self.update_cnt = 0
        self.__current_time = int(time.time() * 1000)

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.model.objects.all().exclude(username="")

    def set_current_time(self):
        self.__current_time = int(time.time() * 1000)

    def create_hmac(self, request_body):
        encoded_data = (
            self.idm_api_url + request_body + self.API_KEY + str(self.__current_time)
        )

        b64mac = base64.b64encode(
            hmac.new(
                self.SECRET_KEY, encoded_data.encode("utf-8"), hashlib.sha1
            ).digest()
        ).decode("ascii")
        return b64mac

    def create_headers(self, b64mac):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-uniffm-apikey": self.API_KEY,
            "x-uniffm-time": str(self.__current_time),
            "x-uniffm-mac": b64mac,
        }

    def prepare_request_body(self):
        """
        Prepare the object for a JSON-RPC request for one user.
        """
        body_obj = {
            "jsonrpc": "2.0",
            "method": "idm.read",
            "id": "1",
            "params": {
                "object": ["shortstamm"],
                "filter": ["db.accountstatus=L"],
                # the "timestamp" is a pseudo filter used by the json-rpc endpoint to filter by "last_changed">"timestamp"
                "datain": {
                    "timestamp": self.last_deprovision_time,
                    "returns": None,
                    "debug": False,
                },
            },
        }
        return json.dumps(body_obj, sort_keys=True)

    def deprovision(self):
        """
        Main method of the deprovisioning process.

        1. Do tasks prior to call the IDM
            1.1 Delete all model instances that full-fill the deprovisioning condition
        2. Prepare data to call the IDM
        3. Handle the response
            3.1 Mark model instances that full-fill the deprovisioning condition for future deletion
        """
        LOGGER.info("Deprovisioning started.")
        self.set_current_time()
        self.pre_deprovision()
        body = self.prepare_request_body()
        headers = self.create_headers(self.create_hmac(body))
        response = requests.post(
            self.idm_api_url, data=body, headers=headers, verify=True
        )
        parsed_content = json.loads(response.content)
        self.handle_response(parsed_content)

    def pre_deprovision(self):
        """
        Hook to handle task prior to the actual deprovision.
        """
        LOGGER.info("PRE-Deprovisioning hook called")
        self.delete_marked_objects()

    def delete_marked_objects(self):
        """
        Delete all model instances where the deprovision_cond_field equals True.
        """
        LOGGER.info("Delete marked objects called.")
        deleted_count = (
            self.get_queryset().filter(**{self.deprovision_cond_field: True}).delete()
        )
        LOGGER.info(f"{deleted_count} User objects deleted.")

    def mark_for_deletion(self, response_body):
        """
        Update the field value of identifier_field for each model instance.
        :param: request_body: JSON parsed response body
        :type: Array[Dict]
        """
        LOGGER.info("mark_for_deletion called")
        with transaction.atomic():
            data = response_body.get("result").get("data")
            logins = [obj["hrzlogin"] for obj in data]
            updated_cnt = self.model.objects.filter(username__in=logins).update(
                **{self.deprovision_cond_field: True}
            )
            self.update_counter(updated_cnt)
        LOGGER.info(f"{self.update_cnt} Objects updated.")
        self.reset_update_cnt()

    def reset_update_cnt(self):
        self.update_cnt = 0

    def update_counter(self, value):
        """
        Method to update the counter of objects.
        :param conditional_value: value used to determine whether an object was actually updated

        Example:
        Changing a field from 1 --> 1 does not count as real update in thos case.
        """
        self.update_cnt += self.get_increment(value)

    def get_increment(self, value):
        """
        Method to determine what increment to provide for the update counter.
        Default to value provided.

        :param conditional_value: value used to determine increment

        Example:
        In this case we will get conditional_value to be True/False --> 1/0

        Can be further generalized in future deprovisioning classes if needed.
        """
        return value

    def handle_response(self, response_body):
        """
        Hook to handle the response body of one Request for the respecting queryset_partition (Size: REQUEST_OBJ_COUNT).
        """
        LOGGER.info("handle_response called.")
        self.mark_for_deletion(response_body)

    def get_update_value(self, obj):
        """
        Method to retrieve the value to update the deprovision_cond_field.
        :param obj: Dictionary of one JSON-RPC Request object
        :type: dict
        """
        assert isinstance(obj, dict)
        return obj["result"]["resultsize"] > 0

    def get_obj_identifier_value(self, obj):
        """
        Method to retrieve the value for the identifier_field.
        :param obj: Dictionary of one JSON-RPC Request object
        :type: dict
        """
        assert isinstance(obj, dict)
        return obj["id"]
