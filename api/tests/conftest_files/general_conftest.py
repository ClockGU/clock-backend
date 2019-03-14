import pytest

from rest_framework.test import APIClient
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
def client():
    return APIClient()
