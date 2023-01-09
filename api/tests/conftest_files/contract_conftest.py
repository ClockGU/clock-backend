import uuid

import pytest
from pytz import datetime
from rest_framework.request import QueryDict

from api.models import Contract
from api.utilities import update_reports

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
    minutes = 1200
    start_date = datetime.date(2019, 1, 1).isoformat()
    end_date = datetime.date(2019, 1, 31).isoformat()
    user = str(user_object.id)

    created_at = datetime.datetime(2018, 12, 31, hour=10).isoformat()
    modified_at = created_at

    data = {
        "name": name,
        "minutes": minutes,
        "start_date": start_date,
        "end_date": end_date,
        "user": user,
        "created_by": user,
        "modified_by": user,
        "created_at": created_at,
        "modified_at": modified_at,
        "initial_carryover_minutes": 0,
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
def contract_ending_in_february_json(valid_contract_json):
    """
    Change the enddate to Februaray 28th.
    Testing that the creation of this contract in March won't work.
    :param valid_contract_json:
    :return:
    """
    valid_contract_json["end_date"] = datetime.date(2019, 2, 28)
    return valid_contract_json


@pytest.fixture
def contract_ending_in_february_querydict(contract_ending_in_february_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(contract_ending_in_february_json)
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
def negative_minutes_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer) JSON dictionary
    where the minutes are negative.
    :param valid_contract_json:
    :return:
    """
    minutes = -1200
    valid_contract_json["minutes"] = minutes
    return valid_contract_json


@pytest.fixture
def negative_minutes_contract_querydict(negative_minutes_contract_json):
    """
    This fixture creates a QueryDict out of the negative_minutes_contract_json.
    :param negative_minutes_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(negative_minutes_contract_json)
    return qdict


@pytest.fixture
def incorrect_carryover_target_date_contract_querydict(
    incorrect_carryover_target_date_contract_json
):
    """
    This fixture creates a QueryDict out of the incorrect_month_start_clocking_contract_json.
    :param incorrect_carryover_target_date_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(incorrect_carryover_target_date_contract_json)
    return qdict


@pytest.fixture
def incorrect_date_carryover_target_date_contract_querydict(
    incorrect_date_carryover_target_date_contract_json
):
    """
    This fixture creates a QueryDict out of the incorrect_date_month_start_clocking_contract_json.
    :param incorrect_date_carryover_target_date_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(incorrect_date_carryover_target_date_contract_json)
    return qdict


@pytest.fixture
def incorrect_carryover_target_date_for_future_contract_json(valid_contract_json):
    """
    This fixture creates an invalid (according to the ContractSerializer) JSON dictionary
    where month_start_clocking date is 1.1.2019 while the contract starts on 1.2.2019.
    :param valid_contract_json:
    :return:
    """
    valid_contract_json["start_date"] = datetime.date(2019, 2, 1).isoformat()
    valid_contract_json["end_date"] = datetime.date(2019, 3, 31).isoformat()
    return valid_contract_json


@pytest.fixture
def incorrect_carryover_target_date_for_future_contract_querydict(
    incorrect_carryover_target_date_for_future_contract_json
):
    """
    This fixture creates a QueryDict out of the incorrect_month_start_clocking_for_future_contract_json.
    :param incorrect_month_start_clocking_for_future_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(incorrect_carryover_target_date_for_future_contract_json)
    return qdict


@pytest.fixture
def non_zero_initial_carryover_minutes_for_future_contract_json(valid_contract_json):
    """
    This fixture creates an invalid (according to the ContractSerializer) JSON dictionary
    where start_carry_over is not timedelta(0) for the contract starting in the future.
    :param valid_contract_json:
    :return:
    """
    valid_contract_json["start_date"] = datetime.date(2019, 2, 1).isoformat()
    valid_contract_json["end_date"] = datetime.date(2019, 3, 31).isoformat()
    valid_contract_json["initial_carryover_minutes"] = 300
    return valid_contract_json


@pytest.fixture
def non_zero_initial_carryover_minutes_for_future_contract_querydict(
    non_zero_initial_carryover_minutes_for_future_contract_json
):
    """
    This fixture creates a QueryDict out of the incorrect_date_month_start_clocking_contract_json.
    :param non_zero_initial_carryover_minutes_for_future_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(non_zero_initial_carryover_minutes_for_future_contract_json)
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
    minutes = 1200
    _start_date = datetime.date(2019, 1, 1)
    _end_date = datetime.date(2019, 1, 31)

    def create_contracts(
        start_stop,
        user,
        start_date=_start_date,
        end_date=_end_date,
        initial_carryover_minutes=0,
    ):
        return [
            Contract.objects.create(
                name=name.format(i),
                minutes=minutes,
                start_date=start_date,
                end_date=end_date,
                initial_carryover_minutes=initial_carryover_minutes,
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
def contract_ending_in_april(create_n_contract_objects, user_object):
    return create_n_contract_objects(
        (1,),
        user_object,
        start_date=datetime.date(2019, 1, 1),
        end_date=datetime.date(2019, 4, 30),
        initial_carryover_minutes=300,
    )[0]


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


@pytest.fixture
def start_date_after_months_with_shifts_contract_json(valid_contract_json):
    """
    This fixture creates an invalid according to the ContractSerializer JSON dictionary.
    Hereby the start_date is inccorect in such a way that after an update there would exist
    shifts outside of the [start_date, end_date] interval.
    :param valid_contract_json:
    :return: Dict
    """
    start_date = datetime.date(2019, 2, 1)
    end_date = datetime.date(2019, 2, 28)
    valid_contract_json["start_date"] = start_date.isoformat()
    valid_contract_json["end_date"] = end_date.isoformat()
    return valid_contract_json


@pytest.fixture
def start_date_after_months_with_shifts_contract_querydict(
    start_date_after_months_with_shifts_contract_json
):
    """
    This fixture creates a QueryDict out of the end_date_before_start_date_contract_json.
    :param start_date_after_months_with_shifts_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(start_date_after_months_with_shifts_contract_json)
    return qdict


@pytest.fixture
def end_date_before_months_with_shifts_contract_json(valid_contract_json):
    """
    This fixture creates an invalid, according to the ContractSerializer, JSON dictionary.
    Hereby the end_date is inccorect in such a way that after an update there would exist
    shifts outside of the [start_date, end_date] interval.
    :param valid_contract_json:
    :return: Dict
    """
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2019, 1, 31)
    valid_contract_json["start_date"] = start_date.isoformat()
    valid_contract_json["end_date"] = end_date.isoformat()
    return valid_contract_json


@pytest.fixture
def end_date_before_months_with_shifts_contract_querydict(
    end_date_before_months_with_shifts_contract_json
):
    """
    This fixture creates a QueryDict out of the end_date_before_start_date_contract_json.
    :param end_date_before_months_with_shifts_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(end_date_before_months_with_shifts_contract_json)
    return qdict


@pytest.fixture
def contract_end_date_7_months_apart_json(valid_contract_json):
    """
    Set the end_date to be more than 6 months apart from the initial end_date.
    :param valid_contract_json:
    :return:
    """
    valid_contract_json["end_date"] = datetime.date(2019, 7, 31).isoformat()
    return valid_contract_json


@pytest.fixture
def contract_locked_shifts(create_n_contract_objects, user_object):
    """
    This fixture provides an a contract, which should have N unlocked not-planned shifts in the first month.
    Those Shifts should trhow an ValidationError during Worktimesheet creation in the next month.
    """
    _start_date = datetime.date(2020, 1, 1)
    _end_date = datetime.date(2020, 2, 29)
    return create_n_contract_objects(
        (1,), start_date=_start_date, end_date=_end_date, user=user_object
    )[0]


@pytest.fixture
def contract_start_mid_january(create_n_contract_objects, user_object):
    """
    Provide contract which starts at the 16. of January and ends in february.
    :param create_n_contract_objects:
    :param user_object:
    :return:
    """
    cont = create_n_contract_objects(
        (1,),
        start_date=datetime.date(2019, 1, 16),
        end_date=datetime.date(2019, 2, 28),
        user=user_object,
    )[0]

    update_reports(cont, datetime.date(2020, 2, 1))  # bring second Report up to date
    return cont


@pytest.fixture
def contract_210h_carryover(create_n_contract_objects, user_object):
    return create_n_contract_objects(
        (1,),
        start_date=datetime.date(2019, 1, 1),
        end_date=datetime.date(2019, 2, 28),
        initial_carryover_minutes=12600,
        user=user_object
    )[0]
