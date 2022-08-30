import pytest
from pytz import datetime, utc
from rest_framework.request import QueryDict

from api.models import ClockedInShift

# This conftest file provides all necessary test data concerning the ClockedInShift Model.
# It will be imported by the conftest.py in the parent directory.


@pytest.fixture
def valid_clockedinshift_json(user_object, contract_object):
    """
    This fixture provides a valid (according to ClockedInShiftSerializer) JSON dictionary for a clocked-in shift
    which is created manually.
    :param user_object:
    :param contract_object:
    :return:
    """
    user = str(user_object.id)
    data = {
        "started": datetime.datetime(2019, 1, 29, 14, tzinfo=utc).isoformat(),
        "contract": str(contract_object.id),
        "user": user,
        "created_by": user,
        "modified_by": user,
    }
    return data

@pytest.fixture
def valid_clockedinshift_sunday_json(user_object, contract_object):
    """
    This fixture provides a valid (according to ClockedInShiftSerializer) JSON dictionary for a clocked-in shift
    which is created manually on a sunday.
    :param user_object:
    :param contract_object:
    :return:
    """
    user = str(user_object.id)
    data = {
        "started": datetime.datetime(2019, 1, 6, 14, tzinfo=utc).isoformat(),
        "contract": str(contract_object.id),
        "user": user,
        "created_by": user,
        "modified_by": user,
    }
    return data

@pytest.fixture
def valid_clockedinshift_holiday_json(user_object, contract_object):
    """
    This fixture provides a valid (according to ClockedInShiftSerializer) JSON dictionary for a clocked-in shift
    which is created manually on a holiday.
    :param user_object:
    :param contract_object:
    :return:
    """
    user = str(user_object.id)
    data = {
        "started": datetime.datetime(2019, 1, 1, 14, tzinfo=utc).isoformat(),
        "contract": str(contract_object.id),
        "user": user,
        "created_by": user,
        "modified_by": user,
    }
    return data

@pytest.fixture
def valid_clockedinshift_querydict(valid_clockedinshift_json):
    """
    This fixture creates a QueryDict out of the valid_shift_json.
    :param valid_clockedinshift_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_clockedinshift_json)
    return qdict

@pytest.fixture
def valid_clockedinshift_sunday_querydict(valid_clockedinshift_sunday_json):
    """
    This fixture creates a QueryDict out of the valid_shift_json.
    :param valid_clockedinshift_sunday_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_clockedinshift_sunday_json)
    return qdict

@pytest.fixture
def valid_clockedinshift_holiday_querydict(valid_clockedinshift_holiday_json):
    """
    This fixture creates a QueryDict out of the valid_shift_json.
    :param valid_clockedinshift_holiday_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(valid_clockedinshift_holiday_json)
    return qdict


@pytest.fixture
def clockedinshift_invalid_contract_json(
    valid_clockedinshift_json, diff_user_contract_object
):
    """
    This fixture creates an invalid according to the ShiftSerializer) JSON dictionary
    where the contract belongs to a different user.
    :param valid_clockedinshift_json:
    :param diff_user_contract_object:
    :return:Dict
    """
    valid_clockedinshift_json["contract"] = str(diff_user_contract_object.id)
    return valid_clockedinshift_json


@pytest.fixture
def clockedinshift_invalid_contract_querydict(clockedinshift_invalid_contract_json):
    """
    This fixture creates a QueryDict out of the contract_not_belonging_to_user_json.
    :param clockedinshift_invalid_contract_json:
    :return: QueryDict
    """
    qdict = QueryDict("", mutable=True)
    qdict.update(clockedinshift_invalid_contract_json)
    return qdict


@pytest.fixture
def update_clockedinshift_json(valid_clockedinshift_json):
    valid_clockedinshift_json["started"] = datetime.datetime(
        2019, 1, 29, 16, tzinfo=utc
    ).isoformat()
    return valid_clockedinshift_json


@pytest.fixture
def clockedinshift_object(user_object, contract_object):
    return ClockedInShift.objects.create(
        started=datetime.datetime(2019, 2, 11, 14, tzinfo=utc),
        user=user_object,
        contract=contract_object,
        created_by=user_object,
        modified_by=user_object,
    )
