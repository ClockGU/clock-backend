import pytest
import uuid
from pytz import datetime
from rest_framework.test import APIClient
from django.urls import reverse

from api.models import User, Contract, Shift, Report


@pytest.fixture
def user_model_class():
    return User


@pytest.fixture
def contract_model_class():
    return Contract


@pytest.fixture
def shift_model_class():
    return Shift


@pytest.fixture
def report_model_class():
    return Report


@pytest.fixture
def user_object():
    return User.objects.create_user(
        email="test@test.com",
        first_name="Testfirstname",
        last_name="Testlastname",
        personal_number="1234567890",
        password="Test_password",
    )


@pytest.fixture
def user_object_password():
    return "Test_password"


@pytest.fixture
def valid_contract_json(user_object):
    name = "Test Contract"
    hours = 20.0
    start_date = datetime.date(2019, 1, 1).isoformat()
    end_date = datetime.date(2019, 1, 31).isoformat()
    user = user_object.id

    created_at = datetime.datetime(2018, 12, 31, hour=10).isoformat()
    modified_at = created_at

    data = {
        "name": name,
        "hours": hours,
        "start_date": start_date,
        "end_date": end_date,
        "user": user,
        "created_by": user,
        "modified_by": user,
        "created_at": created_at,
        "modified_at": modified_at,
    }

    return data


@pytest.fixture
def end_date_before_start_date_contract_json(valid_contract_json):
    start_date = datetime.date(2019, 2, 1)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def start_date_day_incorrect_contract_json(valid_contract_json):
    start_date = datetime.date(2019, 1, 6)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def end_date_day_incorrect_contract_json(valid_contract_json):
    end_date = datetime.date(2019, 1, 22)
    valid_contract_json["end_date"] = end_date
    return valid_contract_json


@pytest.fixture
def negative_hours_contract_json(valid_contract_json):
    hours = -20.0
    valid_contract_json["hours"] = hours
    return valid_contract_json


@pytest.fixture
def invalid_uuid_contract_json(valid_contract_json):
    random_uuid = uuid.uuid4()
    valid_contract_json.pop("user")
    valid_contract_json.pop("created_by")
    valid_contract_json.pop("modified_by")
    valid_contract_json.pop("created_at")
    valid_contract_json.pop("modified_at")
    return valid_contract_json


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_object_jwt(user_object, client, user_object_password):
    user_response = client.post(
        path=reverse("jwt-create"),
        data={"email": user_object.email, "password": user_object_password},
    )

    return user_response.data["access"]
