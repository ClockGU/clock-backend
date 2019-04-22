# This conftest file will be discovered first and summarizes all files in the ./conftest_files directory.
# The conftest file is split up into these files for clarity and brevity.
# Everything is handled according to the pytest documentiation
# found here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
#
import pytest
from celery.contrib.testing.worker import start_worker
from project_celery.celery import app
from api.tests.conftest_files.contract_conftest import *
from api.tests.conftest_files.general_conftest import *
from api.tests.conftest_files.report_conftest import *
from api.tests.conftest_files.shift_conftest import *
from api.tests.conftest_files.user_conftest import *


@pytest.fixture
def celery_test_fixture(user_object, contract_ending_in_february):
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
