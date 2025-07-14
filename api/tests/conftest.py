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

from api.tests.conftest_files.clockedinshift_conftest import *  # noqa
from api.tests.conftest_files.contract_conftest import *  # noqa
from api.tests.conftest_files.deprovision_conftest import *  # noqa
from api.tests.conftest_files.general_conftest import *  # noqa
from api.tests.conftest_files.report_conftest import *  # noqa
from api.tests.conftest_files.shift_conftest import *  # noqa
from api.tests.conftest_files.user_conftest import *  # noqa
from api.tests.conftest_files.carryover_conftest import *  # noqa
