import pytest
import json

from pytz import datetime
from rest_framework.request import QueryDict
from api.models import Shift


@pytest.fixture
def valid_shift_json(user_object, contract_object):
    started = datetime.datetime(2019, 1, 29, 14).isoformat()
    stopped = datetime.datetime(2019, 1, 29, 16).isoformat()
    created_at = datetime.datetime(2019, 1, 29, 16).isoformat()
    modified_at = created_at
    user = user_object.id
    contract = contract_object.id
    _type = "st"
    note = "something was strange"
    tags = json.dumps(["tag1", "tag2"])

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
    valid_shift_json["tags"] = json.dumps([1, [], "a"])
    return valid_shift_json


@pytest.fixture
def tags_not_string_querydict(tags_not_strings_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(tags_not_strings_json)
    return qdict


@pytest.fixture
def shift_starts_before_contract_json(valid_shift_json):
    """
    The contract object has for start_date the 29th of January in 2019.
    :param valid_shift_json:
    :return:
    """
    valid_shift_json["started"] = datetime.datetime(2018, 12, 19, 14)
    valid_shift_json["stopped"] = datetime.datetime(2018, 12, 19, 16)
    return valid_shift_json


@pytest.fixture
def shift_starts_before_contract_querydict(shift_starts_before_contract_json):
    qdict = QueryDict("", mutable=True)
    qdict.update(shift_starts_before_contract_json)
    return qdict


@pytest.fixture
def shift_starts_ends_after_contract_json(valid_shift_json):
    """
    The contract object has for start_date the 29th of January in 2019.
    :param valid_shift_json:
    :return:
    """
    valid_shift_json["started"] = datetime.datetime(2019, 2, 19, 14)
    valid_shift_json["stopped"] = datetime.datetime(2019, 2, 19, 16)
    return valid_shift_json


@pytest.fixture
def shift_starts_ends_after_contract_json_querydict(
    shift_starts_ends_after_contract_json
):
    qdict = QueryDict("", mutable=True)
    qdict.update(shift_starts_ends_after_contract_json)
    return qdict


@pytest.fixture
def create_n_shift_objects():

    started = datetime.datetime(2019, 1, 29, 14)
    stopped = datetime.datetime(2019, 1, 29, 16)
    created_at = datetime.datetime(2019, 1, 29, 16).isoformat()
    modified_at = created_at
    _type = "st"
    note = "something was strange"
    tags = ["tag1, tag2"]

    def create_shifts(start_stop, user, contract):
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
    return create_n_shift_objects((1,), user_object, contract_object)[0]


@pytest.fixture
def db_creation_shifts_list_endpoint(
    user_object,
    diff_user_object,
    contract_object,
    diff_user_contract_object,
    create_n_shift_objects,
):
    # Create 2 shifts for the User
    create_n_shift_objects((1, 3), user=user_object, contract=contract_object)
    # Create another 2 shifts for different User
    create_n_shift_objects(
        (1, 3), user=diff_user_object, contract=diff_user_contract_object
    )


@pytest.fixture
def put_new_tags_json(valid_shift_json, shift_object):
    valid_shift_json["id"] = shift_object.id
    valid_shift_json["tags"] = json.dumps(["new_tag1", "new_tag2"])
    return valid_shift_json

@pytest.fixture
def patch_new_tags_json(shift_object):
    _dict = {
        "id": shift_object.id,
        "tags": json.dumps(["new_tag1", "new_tag2"])
    }
    return _dict
