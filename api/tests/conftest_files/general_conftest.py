import pytest
from django.urls import reverse
from django.test import RequestFactory
from rest_framework.request import QueryDict, Request
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from dateutil.relativedelta import relativedelta

from api.models import Contract, Report, Shift, User
from api.views import ReportViewSet

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


def setup_view(view, request, *args, **kwargs):
    """
    Function to mimic a .as_view() call on a Class-Based-View for testing purposes.
    :param view:
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


@pytest.fixture
def prepared_ReportViewSet_view(report_object):
    factory = RequestFactory()
    request = factory.get(
        reverse("api:reports-export", args=["{}".format(report_object.id)])
    )
    return setup_view(ReportViewSet(), request)


@pytest.fixture
def positive_relativedelta_object():
    return relativedelta(days=6, hours=4, minutes=23, seconds=15)


@pytest.fixture
def negative_relativedelta_object():
    return relativedelta(days=-6, hours=-4, minutes=-23, seconds=-15)
