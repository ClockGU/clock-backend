"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
import pytest
from dateutil.relativedelta import relativedelta
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.request import QueryDict, Request
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from api.models import ClockedInShift, Contract, Report, Shift, User
from api.views import ContractViewSet, ReportViewSet

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
def clockedinshift_model_class():
    return ClockedInShift


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
def prepared_ContractViewSet_view(user_object):
    factory = RequestFactory()
    request = factory.get(reverse("api:contracts-list"))
    request.user = user_object
    return setup_view(ContractViewSet(), request)


@pytest.fixture
def prepared_ReportViewSet_view_mid_january(contract_start_mid_january):
    """
    Prepare
    :param report_object:
    :return:
    """

    report_object = contract_start_mid_january.reports.get(
        month_year=contract_start_mid_january.start_date.replace(day=1)
    )
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


@pytest.fixture
def test_contract_change(
    create_n_contract_objects, create_n_shift_objects, user_object
):
    contracts = create_n_contract_objects((1, 3), user_object)
    create_n_shift_objects((1,), user=user_object, contract=contracts[0])
    return contracts
