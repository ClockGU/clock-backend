import pytest

from api.utilities import relativedelta_to_string


def test_relativedelta_to_string_positive_delta(positive_relativedelta_object):
    result_string = relativedelta_to_string(positive_relativedelta_object)
    assert result_string == "148:23:15"


def test_relativedelta_to_string_negative_delta(negative_relativedelta_object):
    result_string = relativedelta_to_string(negative_relativedelta_object)
    assert result_string == "-148:23:15"
