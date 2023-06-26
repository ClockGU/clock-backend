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


def format_message(url, name, email, message):
    text = (
        f"Name: {name}",
        f"E-Mail: {email}",
        "Nachricht:",
        "",
        message,
        "",
        "---------",
        "",
        f"Das ist eine automatisch generierte Nachricht von Clock (System URL: {url})",
    )

    return "\n".join(text)
