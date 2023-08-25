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
import freezegun
import pytest

from api.idm.deprovisioning import Deprovisioner


@pytest.fixture
def deprovision_test_users(create_n_user_objects):
    """
    Create 10 User objects to test the Derpovisioner class.
    """
    return create_n_user_objects((10,))


@pytest.fixture
def first_deprovision_test_user(deprovision_test_users):
    return deprovision_test_users[0]


@pytest.fixture
def test_deprovisioner_instance():
    """
    Set the REQUEST_OBJ_COUNT to 2 for testing of request Partition.
    (By doing that we avoid creating 501 User objects.)
    """
    deprovisioner = Deprovisioner()
    deprovisioner.REQUEST_OBJ_COUNT = 2
    return deprovisioner


@pytest.fixture
def not_deleted_user_json_rpc_obj(first_deprovision_test_user):
    return {
        "jsonrpc": "2.0",
        "id": f"{first_deprovision_test_user.username}",
        "result": {
            "resultsize": 0,
            "success": True,
            "hasInfos": True,
            "hasWarnings": False,
            "hasErrors": False,
            "hasFatals": False,
            "hasStrangeMessage": False,
            "data": [],
            "messages": [
                {
                    "messageID": "IOK",
                    "messageType": "INFO",
                    "messageData": "Ausfuehrung erfolgreich.",
                }
            ],
        },
    }
