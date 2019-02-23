import pytest
from pytz import datetime


@pytest.fixture
def valid_shift_json(user_object, contract_object):
    started = datetime.datetime(2019, 1, 29, 14)
    stopped = datetime.date(2019, 1, 29, 16)
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
