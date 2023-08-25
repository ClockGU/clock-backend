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
import datetime
import json
import time

import pytest

from api.idm.deprovisioning import Deprovisioner


class TestClassAttributes:
    instance = Deprovisioner()

    # Test for existing Attributes
    def test_has_model(self):
        assert hasattr(self.instance, "model")

    def test_has_req_obj_count(self):
        assert hasattr(self.instance, "REQUEST_OBJ_COUNT")

    def test_has_identifier_field(self):
        assert hasattr(self.instance, "identifier_field")

    def test_has_deprovision_cond_field(self):
        assert hasattr(self.instance, "deprovision_cond_field")

    def test_has_update_cnt(self):
        assert hasattr(self.instance, "update_cnt")

    def test_has_idm_api_url(self):
        assert hasattr(self.instance, "idm_api_url")

    def test_has_api_key(self):
        assert hasattr(self.instance, "API_KEY")

    def test_has_secret_key(self):
        assert hasattr(self.instance, "SECRET_KEY")

    def test_has_queryset(self):
        assert hasattr(self.instance, "queryset")

    def test_has_request_bodies(self):
        assert hasattr(self.instance, "request_bodies")

    def test_has_time(self):
        assert hasattr(self.instance, "time")

    # Test for existing methods
    def test_has_get_model(self):
        assert hasattr(self.instance, "get_model")
        assert callable(getattr(self.instance, "get_model"))

    def test_has_get_queryset(self):
        assert hasattr(self.instance, "get_queryset")
        assert callable(getattr(self.instance, "get_queryset"))

    def test_has_create_hmac(self):
        assert hasattr(self.instance, "create_hmac")
        assert callable(getattr(self.instance, "create_hmac"))

    def test_has_create_headers(self):
        assert hasattr(self.instance, "create_headers")
        assert callable(getattr(self.instance, "create_headers"))

    def test_has_prepare_request_bodies(self):
        assert hasattr(self.instance, "prepare_request_bodies")
        assert callable(getattr(self.instance, "prepare_request_bodies"))

    def test_has_prepare_obj_json_rpc(self):
        assert hasattr(self.instance, "prepare_obj_json_rpc")
        assert callable(getattr(self.instance, "prepare_obj_json_rpc"))

    def test_has_deprovision(self):
        assert hasattr(self.instance, "deprovision")
        assert callable(getattr(self.instance, "deprovision"))

    def test_has_handle_response(self):
        assert hasattr(self.instance, "handle_response")
        assert callable(getattr(self.instance, "handle_response"))

    def test_has_pre_deprovision_hook(self):
        assert hasattr(self.instance, "pre_deprovision")
        assert callable(getattr(self.instance, "pre_deprovision"))

    def test_has_delete_marked_objects(self):
        assert hasattr(self.instance, "delete_marked_objects")
        assert callable(getattr(self.instance, "delete_marked_objects"))

    def test_has_mark_for_deletion(self):
        assert hasattr(self.instance, "mark_for_deletion")
        assert callable(getattr(self.instance, "mark_for_deletion"))

    def test_has_reset_update_cnt(self):
        assert hasattr(self.instance, "reset_update_cnt")
        assert callable(getattr(self.instance, "reset_update_cnt"))

    def test_has_update_counter(self):
        assert hasattr(self.instance, "update_counter")
        assert callable(getattr(self.instance, "update_counter"))

    def test_has_get_increment(self):
        assert hasattr(self.instance, "get_increment")
        assert callable(getattr(self.instance, "get_increment"))

    def test_has_get_update_value(self):
        assert hasattr(self.instance, "get_update_value")
        assert callable(getattr(self.instance, "get_update_value"))

    def test_has_get_obj_identifier_value(self):
        assert hasattr(self.instance, "get_obj_identifier_value")
        assert callable(getattr(self.instance, "get_obj_identifier_value"))


class TestDeprovisionSteps:
    @pytest.mark.django_db
    def test_request_batch_size(
        self, deprovision_test_users, test_deprovisioner_instance
    ):
        test_deprovisioner_instance.prepare_request_bodies()
        assert len(test_deprovisioner_instance.request_bodies) == 5
        assert all(
            map(
                lambda x: len(json.loads(x)) == 2,
                test_deprovisioner_instance.request_bodies,
            )
        )

    @pytest.mark.freeze_time("2012-01-14")
    @pytest.mark.django_db
    def test_correct_obj_json_rpc(
        self, first_deprovision_test_user, test_deprovisioner_instance
    ):
        body = test_deprovisioner_instance.prepare_obj_json_rpc(
            first_deprovision_test_user
        )
        frozen_unix_epoch = int(time.time() * 1000)
        correct_body = {
            "jsonrpc": "2.0",
            "method": "idm.read",
            "id": "testusername0",
            "params": {
                "object": ["shortstamm"],
                "filter": [f"db.hrzlogin=testusername0 && db.accountstatus=L"],
                "datain": {
                    "timestamp": frozen_unix_epoch,
                    "returns": None,
                    "debug": False,
                },
            },
        }
        assert body == correct_body

    @pytest.mark.django_db
    def test_get_update_value_for_non_deletion(self, test_deprovisioner_instance, not_deleted_user_json_rpc_obj):
        """
        Test whether the method `get_update_value` returns the correct value if the resultsize is 0.

        Expected: get_update_value(not_deleted_user_json_rpc_obj) == False

        Resultsize zero resembles the state when a user is not marked for deletion in the IDM.
        """
        assert not test_deprovisioner_instance.get_update_value(not_deleted_user_json_rpc_obj)

    @pytest.mark.django_db
    def test_get_obj_identifier_value(self, first_deprovision_test_user, test_deprovisioner_instance, not_deleted_user_json_rpc_obj):
        """
        Test whether the method `get_obj_identifier_value` retrieves the
        """
        assert first_deprovision_test_user.username == test_deprovisioner_instance.get_obj_identifier_value(not_deleted_user_json_rpc_obj)
