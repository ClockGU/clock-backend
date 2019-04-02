import pytest

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request, QueryDict
from django.urls import reverse

from api.models import User, Contract, Shift, Report


# This conftest file provides all necessary test data concerning project classes and auxiliary functions/classes.
# It will be imported by the conftest.py in the parent directory.


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


@pytest.fixture
def plain_request_object(user_object):
    """
    This fixture provides a plain request object.
    :param user_object:
    :return:
    """
    request = APIRequestFactory().get(reverse("user-me"), data=QueryDict())
    force_authenticate(request, user=user_object)
    return Request(request)
