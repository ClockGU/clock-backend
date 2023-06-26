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
from ..utils import format_message


def test_format_message():
    output = format_message(
        "http://example.com/feedback",
        "Max Mustermann",
        "max@example.com",
        "Das ist eine Nachricht.",
    )

    expected_one_line = "Name: Max MustermannE-Mail: max@example.comNachricht:Das ist eine Nachricht.---------Das ist eine automatisch generierte Nachricht von Clock (System URL: http://example.com/feedback)"

    output_one_line = "".join([line.replace("\n", "") for line in output.rstrip()])

    assert output_one_line == expected_one_line
