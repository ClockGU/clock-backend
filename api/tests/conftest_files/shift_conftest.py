import pytest
from pytz import datetime
from rest_framework.request import QueryDict


@pytest.fixture
def valid_shift_json(user_object, contract_object):
    started = datetime.datetime(2019, 1, 29, 14)
    stopped = datetime.datetime(2019, 1, 29, 16)
    created_at = datetime.datetime(2019, 1, 29, 16).isoformat()
    modified_at = created_at
    user = user_object.id
    contract = contract_object.id
    _type = "st"
    note = "something was strange"
    tags = ["tag1, tag2"]

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
    }
    return data


@pytest.fixture
def valid_shift_querydict(valid_shift_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_shift_json)
    return qdict


@pytest.fixture
def stopped_before_started_json(valid_shift_json):
    valid_shift_json["started"] = datetime.datetime(2019, 1, 29, 16)
    valid_shift_json["stopped"] = datetime.datetime(2019, 1, 29, 14)
    return valid_shift_json


@pytest.fixture
def stopped_before_started_querydict(stopped_before_started_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(stopped_before_started_json)
    return qdict


@pytest.fixture
def stopped_on_next_day_json(valid_shift_json):
    valid_shift_json["stopped"] = datetime.datetime(2019, 1, 30, 1)
    return valid_shift_json


@pytest.fixture
def stopped_on_next_day_querydict(stopped_on_next_day_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(stopped_on_next_day_json)
    return qdict


@pytest.fixture
def contract_not_belonging_to_user_json(valid_shift_json, diff_user_contract_object):
    valid_shift_json["contract"] = diff_user_contract_object.id
    return valid_shift_json


@pytest.fixture
def contract_not_belonging_to_user_querydict(contract_not_belonging_to_user_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(contract_not_belonging_to_user_json)
    return qdict


@pytest.fixture
def wrong_type_json(valid_shift_json):
    """
    Set an incorrect value for 'type'.
    Allowed types ar : st, sk, and vn.
    :param valid_shift_json:
    :return:
    """
    valid_shift_json["type"] = "xy"
    return valid_shift_json


@pytest.fixture
def wrong_type_querydict(wrong_type_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(wrong_type_json)
    return qdict


@pytest.fixture
def tags_not_strings_json(valid_shift_json):
    valid_shift_json["tags"] = [1, [], "a"]
    return valid_shift_json


@pytest.fixture
def tags_not_string_querydict(tags_not_strings_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(tags_not_strings_json)
    return qdict
