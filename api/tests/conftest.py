import pytest
import uuid
from pytz import datetime
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework.request import Request, QueryDict
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
def create_n_user_objects():
    email = "test{}@test.com"
    first_name = "Testfirstname"
    last_name = "Testlastname"
    personal_number = "1234567890"
    password = "Test_password"

    def create_users(start_stop):
        return [
            User.objects.create_user(
                email=email.format(i),
                first_name=first_name,
                last_name=last_name,
                personal_number=personal_number,
                password=password,
            )
            for i in range(*start_stop)
        ]

    return create_users


@pytest.fixture
def user_object(create_n_user_objects):
    """
    This Fixture creates a user object which resembles the standart user.
    The standart user symbolize the user sending requests to the api.
    :param create_n_user_objects:
    :return: User
    """
    return create_n_user_objects((1,))[0]


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
def valid_contract_querydict(valid_contract_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_contract_json)
    return qdict


@pytest.fixture
def end_date_before_start_date_contract_json(valid_contract_json):
    start_date = datetime.date(2019, 2, 1)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def end_date_before_start_date_contract_querydict(
    end_date_before_start_date_contract_json
):
    qdict = QueryDict("", mutable=True)
    qdict.update(end_date_before_start_date_contract_json)
    return qdict


@pytest.fixture
def start_date_day_incorrect_contract_json(valid_contract_json):
    start_date = datetime.date(2019, 1, 6)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def start_date_day_incorrect_contract_querydict(start_date_day_incorrect_contract_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(start_date_day_incorrect_contract_json)
    return qdict


@pytest.fixture
def end_date_day_incorrect_contract_json(valid_contract_json):
    end_date = datetime.date(2019, 1, 22)
    valid_contract_json["end_date"] = end_date
    return valid_contract_json


@pytest.fixture
def end_date_day_incorrect_contract_querydict(end_date_day_incorrect_contract_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(end_date_day_incorrect_contract_json)
    return qdict


@pytest.fixture
def negative_hours_contract_json(valid_contract_json):
    hours = -20.0
    valid_contract_json["hours"] = hours
    return valid_contract_json


@pytest.fixture
def negative_hours_contract_querydict(negative_hours_contract_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(negative_hours_contract_json)
    return qdict


@pytest.fixture
def invalid_uuid_contract_json(valid_contract_json):
    random_uuid = uuid.uuid4()
    valid_contract_json["user"] = random_uuid
    valid_contract_json["created_by"] = random_uuid
    valid_contract_json["modified_by"] = random_uuid
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


@pytest.fixture
def create_n_contract_objects(user_object):
    name = "Test Contract{}"
    hours = 20.0
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2019, 1, 31)

    def create_contracts(start_stop, user):
        return [
            Contract.objects.create(
                name=name.format(i),
                hours=hours,
                start_date=start_date,
                end_date=end_date,
                user=user,
                created_by=user,
                modified_by=user,
            )
            for i in range(*start_stop)
        ]

    return create_contracts


@pytest.fixture
def contract_object(user_object, create_n_contract_objects):
    """
    This Fixture creates a contract object which resembles the standart contract.
    The standart contract belongs to the standart User.
    :param user_object:
    :param create_n_contract_objects:
    :return:
    """
    return create_n_contract_objects((1,), user_object)[0]


@pytest.fixture
def diff_user_object(create_n_user_objects):
    return create_n_user_objects((1, 2))[0]


@pytest.fixture
def diff_user_contract_object(create_n_contract_objects, diff_user_object):
    return create_n_contract_objects((1, 2), diff_user_object)[0]


@pytest.fixture
def db_creation_contracts_list_endpoint(
    user_object, create_n_user_objects, create_n_contract_objects, diff_user_object
):
    # Create 2 contracts for the User to test
    create_n_contract_objects((1, 3), user_object)
    # Create another user and 2 Contracts for him
    create_n_contract_objects((1, 3), diff_user_object)


@pytest.fixture
def invalid_uuid_contract_put_endpoint(invalid_uuid_contract_json, contract_object):
    invalid_uuid_contract_json["id"] = contract_object.id
    return invalid_uuid_contract_json


@pytest.fixture
def invalid_uuid_contract_patch_endpoint(contract_object):
    random_uuid = uuid.uuid4()
    _dict = {
        "id": contract_object.id,
        "user": random_uuid,
        "created_by": random_uuid,
        "modified_by": random_uuid,
    }
    return _dict


@pytest.fixture
def plain_request_object(user_object):
    request = APIRequestFactory().get(reverse("user-me"), data=QueryDict())
    force_authenticate(request, user=user_object)
    return Request(request)
