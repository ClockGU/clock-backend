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
from django.core.management.base import BaseCommand, CommandError

from api.models import Shift, User


class Command(BaseCommand):
    help = "Unlock month in specified year for given user."

    def add_arguments(self, parser):
        parser.add_argument("month", type=int)

        parser.add_argument("year", type=int)

        parser.add_argument("user_id", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(id=options["user_id"])

        if user is None:
            raise CommandError("User ID is not defined.")

        shifts = Shift.objects.filter(
            user=user, started__month=options["month"], started__year=options["year"]
        )
        shifts.update(locked=False)
        self.stdout.write(
            self.style.SUCCESS(
                f"All Shifts in {options['month']}.{options['year']} (MM.YYYY) are unlocked."
            )
        )
