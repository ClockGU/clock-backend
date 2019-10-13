import uuid

import pytest
from pytz import datetime
from rest_framework.request import QueryDict

from api.models import Contract

# This conftest file provides all necessary test data concerning the Contract Model.
# It will be imported by the conftest.py in the parent directory.


@pytest.fixture
def valid_contract_json(user_object):
    """
    This fixture provides a valid (according to the ContractSerializer) JSON dictionary.
    :param user_object:
    :param user_object:
    :return: Dict
    """
    name = "Test Contract"
    hours = 20.0
    start_date = datetime.date(2019, 1, 1).isoformat()
    end_date = datetime.date(2019, 1, 31).isoformat()
    user = str(user_object.id)

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
    """
    This fixture creates a QueryDict out of the valid_contract_json.
    :param valid_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_contract_json)
    return qdict


@pytest.fixture
def end_date_before_start_date_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the end_date datetime is before the start_date datetime.
    :param valid_contract_json:
    :return: Dict
    """
    start_date = datetime.date(2019, 2, 1)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def end_date_before_start_date_contract_querydict(
    end_date_before_start_date_contract_json
):
    """
    This fixture creates a QueryDict out of the end_date_before_start_date_contract_json.
    :param end_date_before_start_date_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(end_date_before_start_date_contract_json)
    return qdict


@pytest.fixture
def start_date_day_incorrect_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the start_date day is invalid.
    :param valid_contract_json:
    :return: Dict
    """
    start_date = datetime.date(2019, 1, 6)
    valid_contract_json["start_date"] = start_date
    return valid_contract_json


@pytest.fixture
def start_date_day_incorrect_contract_querydict(start_date_day_incorrect_contract_json):
    """
    This fixture creates a QueryDict out of the start_date_day_incorrect_contract_json.
    :param start_date_day_incorrect_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(start_date_day_incorrect_contract_json)
    return qdict


@pytest.fixture
def end_date_day_incorrect_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the end_date day is invalid.
    :param valid_contract_json:
    :return: Dict
    """
    end_date = datetime.date(2019, 1, 22)
    valid_contract_json["end_date"] = end_date
    return valid_contract_json


@pytest.fixture
def end_date_day_incorrect_contract_querydict(end_date_day_incorrect_contract_json):
    """
    This fixture creates a QueryDict out of the end_date_day_incorrect_contract_json.
    :param end_date_day_incorrect_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(end_date_day_incorrect_contract_json)
    return qdict


@pytest.fixture
def negative_hours_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the hours are negative.
    :param valid_contract_json:
    :return:
    """
    hours = -20.0
    valid_contract_json["hours"] = hours
    return valid_contract_json


@pytest.fixture
def negative_hours_contract_querydict(negative_hours_contract_json):
    """
    This fixture creates a QueryDict out of the negative_hours_contract_json.
    :param negative_hours_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(negative_hours_contract_json)
    return qdict


@pytest.fixture
def invalid_uuid_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the user Uuid is set to a different (random) one.
    :param valid_contract_json:
    :return: Dict
    """
    random_uuid = str(uuid.uuid4())
    valid_contract_json["user"] = random_uuid
    valid_contract_json["created_by"] = random_uuid
    valid_contract_json["modified_by"] = random_uuid
    valid_contract_json.pop("created_at")
    valid_contract_json.pop("modified_at")
    return valid_contract_json


@pytest.fixture
def create_n_contract_objects(user_object):
    """
    This fixture resembles a contract object factory.
    Shifts are distinguised by id, there is no specific need for the start_stop mechanism.
    Nonetheless we distinguish them by name too.
    :return: Function
    """
    name = "Test Contract{}"
    hours = 20.0
    _start_date = datetime.date(2019, 1, 1)
    _end_date = datetime.date(2019, 1, 31)

    def create_contracts(start_stop, user, start_date=_start_date, end_date=_end_date):
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
    This fixture creates a contract object which resembles the standart contract.
    The standart contract belongs to the standart User.
    :param user_object:
    :param create_n_contract_objects:
    :return:
    """
    return create_n_contract_objects((1,), user_object)[0]


@pytest.fixture
def report_update_contract(create_n_contract_objects, report_update_user):
    return create_n_contract_objects(
        (1,),
        report_update_user,
        start_date=datetime.date(2019, 1, 1),
        end_date=datetime.date(2019, 2, 28),
    )[0]


@pytest.fixture
def contract_ending_in_february(create_n_contract_objects, user_object):
    end_date = datetime.date(2019, 2, 28)
    return create_n_contract_objects((1,), user_object, end_date=end_date)[0]


@pytest.fixture
def contract_ending_in_february_test_update_version(
    create_n_contract_objects, user_object
):
    end_date = datetime.date(2019, 2, 28)
    return create_n_contract_objects((1,), user_object, end_date=end_date)[0]


@pytest.fixture
def diff_user_contract_object(create_n_contract_objects, diff_user_object):
    """
    This fixture creates a contract object for a different user.
    :param create_n_contract_objects:
    :param diff_user_object:
    :return:
    """
    return create_n_contract_objects((1, 2), diff_user_object)[0]


@pytest.fixture
def db_creation_contracts_list_endpoint(
    user_object, create_n_user_objects, create_n_contract_objects, diff_user_object
):
    """
    This fixture creates two contract objects for the standart user and two for a different user.
    :param user_object:
    :param create_n_user_objects:
    :param create_n_contract_objects:
    :param diff_user_object:
    :return:
    """
    # Create 2 contracts for the User to test
    create_n_contract_objects((1, 3), user_object)
    # Create another user and 2 Contracts for him
    create_n_contract_objects((1, 3), diff_user_object)


@pytest.fixture
def invalid_uuid_contract_put_endpoint(invalid_uuid_contract_json, contract_object):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the user Uuid is set to a different (random) one but the contract id is correct.
    It is used to test wether a PUT is succesfull to change the user/owner of a contract.
    :param invalid_uuid_contract_json:
    :param contract_object:
    :return: Dict
    """
    invalid_uuid_contract_json["id"] = str(contract_object.id)
    return invalid_uuid_contract_json


@pytest.fixture
def invalid_uuid_contract_patch_endpoint(contract_object):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the user Uuid is set to a different (random) one but the contract id is correct.
    It is used to test wether a PATCH is succesfull to change the user/owner of a contract.
    :param contract_object:
    :return: Dict
    """
    random_uuid = str(uuid.uuid4())
    _dict = {
        "id": str(contract_object.id),
        "user": random_uuid,
        "created_by": random_uuid,
        "modified_by": random_uuid,
    }
    return _dict
