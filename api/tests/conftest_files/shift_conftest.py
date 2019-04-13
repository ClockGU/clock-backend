import json

import pytest
from pytz import datetime, utc
from rest_framework.request import QueryDict

from api.models import Shift

# This conftest file provides all necessary test data concerning the Shift Model.
# It will be imported by the conftest.py in the parent directory.


@pytest.fixture
def valid_shift_json(user_object, contract_object):
    """
    This fixture provides a valid (according to the ShiftSerializer) JSON dictionary for a shift
    which is created manually (for the past) or was 'gestochen'.
    :param user_object:
    :param contract_object:
    :return: Dict
    """
    started = datetime.datetime(2019, 1, 29, 14, tzinfo=utc).isoformat()
    stopped = datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat()
    created_at = datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat()
    modified_at = created_at
    user = user_object.id
    contract = contract_object.id
    _type = "st"
    note = "something was strange"
    tags = json.dumps(["tag1", "tag2"])
    was_reviewed = True

    data = {
        "started": started,
        "stopped": stopped,
        "contract": contract,
        "type": _type,
        "note": note,
        "tags": tags,
        "user": user,
        "created_by": user,
        "modified_by": user,
        "created_at": created_at,
        "modified_at": modified_at,
        "was_reviewed": was_reviewed,
    }
    return data


@pytest.fixture
def valid_shift_querydict(valid_shift_json):
    """
    This fixture creates a QueryDict out of the valid_shift_json.
    :param valid_shift_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_shift_json)
    return qdict


@pytest.fixture
def stopped_before_started_json(valid_shift_json):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary
    where the started datatime is after the stopped datetime.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["started"] = datetime.datetime(2019, 1, 29, 16, tzinfo=utc)
    valid_shift_json["stopped"] = datetime.datetime(2019, 1, 29, 14, tzinfo=utc)
    return valid_shift_json


@pytest.fixture
def stopped_before_started_querydict(stopped_before_started_json):
    """
    This fixture creates a QueryDict out of the stopped_before_started_json.
    :param stopped_before_started_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(stopped_before_started_json)
    return qdict


@pytest.fixture
def stopped_on_next_day_json(valid_shift_json):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary
    where the stopped datetime is on the next day after the started datetime.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["stopped"] = datetime.datetime(2019, 1, 30, 1, tzinfo=utc)
    return valid_shift_json


@pytest.fixture
def stopped_on_next_day_querydict(stopped_on_next_day_json):
    """
    This fixture creates a QueryDict out of the stopped_on_next_day_json.
    :param stopped_on_next_day_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(stopped_on_next_day_json)
    return qdict


@pytest.fixture
def contract_not_belonging_to_user_json(valid_shift_json, diff_user_contract_object):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary
    where the contract belongs to a different user.
    :param valid_shift_json:
    :param diff_user_contract_object:
    :return:Dict
    """
    valid_shift_json["contract"] = diff_user_contract_object.id
    return valid_shift_json


@pytest.fixture
def contract_not_belonging_to_user_querydict(contract_not_belonging_to_user_json):
    """
    This fixture creates a QueryDict out of the contract_not_belonging_to_user_json.
    :param contract_not_belonging_to_user_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(contract_not_belonging_to_user_json)
    return qdict


@pytest.fixture
def wrong_type_json(valid_shift_json):
    """
    Set an incorrect value for 'type'.
    Allowed types ar : st, sk, and vn.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["type"] = "xy"
    return valid_shift_json


@pytest.fixture
def wrong_type_querydict(wrong_type_json):
    """
    This fixture creates a QueryDict out of the wrong_type_json.
    :param wrong_type_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(wrong_type_json)
    return qdict


@pytest.fixture
def tags_not_strings_json(valid_shift_json):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary
    where the tags do not solely consist of strings.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["tags"] = json.dumps([1, [], "a"])
    return valid_shift_json


@pytest.fixture
def tags_not_string_querydict(tags_not_strings_json):
    """
    This fixture creates a QueryDict out of the tags_not_strings_json.
    :param tags_not_strings_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(tags_not_strings_json)
    return qdict


@pytest.fixture
def shift_starts_before_contract_json(valid_shift_json):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary.
    Here the started and stopped of the shift are set before the contract starts.
    The contract object has for start_date the 1st of January in 2019.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["started"] = datetime.datetime(2018, 12, 19, 14, tzinfo=utc)
    valid_shift_json["stopped"] = datetime.datetime(2018, 12, 19, 16, tzinfo=utc)
    return valid_shift_json


@pytest.fixture
def shift_starts_before_contract_querydict(shift_starts_before_contract_json):
    """
    This fixture creates a QueryDict out of the shift_starts_before_contract_json.
    :param shift_starts_before_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(shift_starts_before_contract_json)
    return qdict


@pytest.fixture
def shift_starts_ends_after_contract_json(valid_shift_json):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary.
    Here the started and stopped of the shift are set after the contract ends.
    The contract object has for end_date the 31st of January in 2019.
    :param valid_shift_json:
    :return: Dict
    """
    valid_shift_json["started"] = datetime.datetime(2019, 2, 19, 14, tzinfo=utc)
    valid_shift_json["stopped"] = datetime.datetime(2019, 2, 19, 16, tzinfo=utc)
    return valid_shift_json


@pytest.fixture
def shift_starts_ends_after_contract_json_querydict(
    shift_starts_ends_after_contract_json
):
    """
    This fixture creates a QueryDict out of the shift_starts_ends_after_contract_json.
    :param shift_starts_ends_after_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(shift_starts_ends_after_contract_json)
    return qdict


@pytest.fixture
def shift_is_planned_but_started_in_past_json(valid_shift_json):
    valid_shift_json["was_reviewed"] = False
    return valid_shift_json


@pytest.fixture
def shift_is_planned_but_started_in_past_json_querydict(
    shift_is_planned_but_started_in_past_json
):
    qdict = QueryDict("", mutable=True)
    qdict.update(shift_is_planned_but_started_in_past_json)
    return qdict


@pytest.fixture
def create_n_shift_objects():
    """
    This fixture resembles a shift object factory.
    Shifts are distinguised by id, there is no specific need for the start_stop mechanism.
    Nonetheless in terms of consistency this mechanism is kept as in the user_conftest.py.
    :return: Function
    """
    _started = datetime.datetime(2019, 1, 29, 14, tzinfo=utc)
    _stopped = datetime.datetime(2019, 1, 29, 16, tzinfo=utc)
    created_at = datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat()
    modified_at = created_at
    _type = "st"
    note = "something was strange"
    tags = ["tag1, tag2"]

    def create_shifts(start_stop, user, contract, started=_started, stopped=_stopped):
        lst = []
        for i in range(*start_stop):
            shift = Shift.objects.create(
                started=started,
                stopped=stopped,
                created_at=created_at,
                modified_at=modified_at,
                type=_type,
                note=note,
                user=user,
                created_by=user,
                modified_by=user,
                contract=contract,
            )
            shift.tags.add(*tags)
            lst.append(shift)
        return lst

    return create_shifts


@pytest.fixture
def shift_object(create_n_shift_objects, user_object, contract_object):
    """
    This fixture creats one shift object.
    :param create_n_shift_objects:
    :param user_object:
    :param contract_object:
    :return: Shift
    """
    return create_n_shift_objects((1,), user_object, contract_object)[0]


@pytest.fixture
def db_creation_shifts_list_endpoint(
    user_object,
    diff_user_object,
    contract_object,
    diff_user_contract_object,
    create_n_shift_objects,
):
    """
    This fixture crates 2 shifts for the standart user and 2 shifts for a different user.
    :param user_object:
    :param diff_user_object:
    :param contract_object:
    :param diff_user_contract_object:
    :param create_n_shift_objects:
    :return: None
    """
    # Create 2 shifts for the User
    create_n_shift_objects((1, 3), user=user_object, contract=contract_object)
    # Create another 2 shifts for different User
    create_n_shift_objects(
        (1, 3), user=diff_user_object, contract=diff_user_contract_object
    )


@pytest.fixture
def put_new_tags_json(valid_shift_json, shift_object):
    """
    This fixture prepares a JSON dictionary to PUT new tags in a shift.
    :param valid_shift_json:
    :param shift_object:
    :return: Dict
    """
    valid_shift_json["id"] = shift_object.id
    valid_shift_json["tags"] = json.dumps(["new_tag1", "new_tag2"])
    return valid_shift_json


@pytest.fixture
def patch_new_tags_json(shift_object):
    """
    This fixture prepares a JSON dictionary to PATCH new tags in a shift.
    :param shift_object:
    :return: Dict
    """
    _dict = {"id": shift_object.id, "tags": json.dumps(["new_tag1", "new_tag2"])}
    return _dict


@pytest.fixture
def db_creation_list_month_year_endpoint(
    db_creation_shifts_list_endpoint,
    user_object,
    contract_object,
    create_n_shift_objects,
):
    """
    This fixture creates 2 shifts for the standart user on the 2nd of February 2019
    :param db_creation_shifts_list_endpoint:
    :param user_object:
    :param contract_object:
    :param create_n_shift_objects:
    :return:
    """
    # dependency of db_creation_shifts_list_endpoint creates 2 shifts for user_object on 29th of January
    # and 2 shifts for diff user_object also on 29th of January
    # We now create 2 shift on 2nd of February for user_object
    _started = datetime.datetime(2019, 2, 2, 14, tzinfo=utc)
    _stopped = datetime.datetime(2019, 2, 2, 16, tzinfo=utc)
    create_n_shift_objects(
        (1, 3),
        user=user_object,
        contract=contract_object,
        started=_started,
        stopped=_stopped,
    )
