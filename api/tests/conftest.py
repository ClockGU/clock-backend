# This conftest file will be discovered first and summarizes all files in the ./conftest_files directory.
# The conftest file is split up into these files for clarity and brevity.
# Everything is handled according to the pytest documentiation
# found here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
#

from api.tests.conftest_files.contract_conftest import *
from api.tests.conftest_files.general_conftest import *
from api.tests.conftest_files.report_conftest import *
from api.tests.conftest_files.shift_conftest import *
from api.tests.conftest_files.user_conftest import *


@pytest.fixture
def contract_update_fixture(
    user_object, contract_ending_in_february, create_n_report_objects
):
    january_report = create_n_report_objects(
        (1,),
        user_object,
        contract_ending_in_february,
        hours=datetime.timedelta(hours=22),
        month_year=datetime.date(2019, 1, 1),
    )[0]

    february_report = create_n_report_objects(
        (1,),
        user_object,
        contract_ending_in_february,
        hours=datetime.timedelta(hours=2),
        month_year=datetime.date(2019, 2, 1),
    )[0]
