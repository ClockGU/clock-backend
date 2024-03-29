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
# This conftest file will be discovered first and summarizes all files in the ./conftest_files directory.
# The conftest file is split up into these files for clarity and brevity.
# Everything is handled according to the pytest documentiation
# found here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions

from celery.contrib.testing.worker import start_worker

from api.tests.conftest import *  # noqa
from project_celery.celery import app


@pytest.fixture
def december_contract(user_object):
    return Contract.objects.create(
        name="Test Contract",
        minutes=1200,
        start_date=datetime.date(2019, 12, 1),
        end_date=datetime.date(2020, 2, 29),
        initial_carryover_minutes=0,
        user=user_object,
        created_by=user_object,
        modified_by=user_object,
        worktime_model_name="studEmp",
    )


@pytest.fixture
def celery_test_fixture(user_object):
    """
    This Fixture starts a celery worker in the running test container and exits it.
    With this manual entering and exiting it is possible to use the time set by freezgun and also
    use the Testdatabase.
    :param user_object:
    :param contract_ending_in_february:
    :return:
    """
    worker = start_worker(app)
    worker.__enter__()
    yield
    worker.__exit__(None, None, None)


@pytest.fixture
def celery_test_fixture_correct_minutes(user_object, contract_ending_in_february):
    """
    This fixture modifies the automatically created report for January to have symbolicaly 600 minutes of work
    documented. It is needed to test whether the automatic Report creation carries over the minutes of
    the last month.
    :param user_object:
    :param contract_ending_in_february:
    :return:
    """
    january_report = contract_ending_in_february.reports.get(month_year__month=1)
    january_report.worktime = datetime.timedelta(minutes=600)
    january_report.save()
    worker = start_worker(app)
    worker.__enter__()
    yield
    worker.__exit__(None, None, None)


@pytest.fixture
def celery_test_fixture_end_of_year_test(december_contract):
    """
    This fixture creates a Contract which starts on 1.1.2019 and ends at 29.2.2020.
    The expected output is as in every other month: -1200 minutes on the automatically created Report at the beginning
    of a month.

    :param december_contract:
    :return:
    """

    worker = start_worker(app)
    worker.__enter__()
    yield
    worker.__exit__(None, None, None)
