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
import datetime

from django.core.management.base import BaseCommand

from api.models import Contract
from api.utilities import update_reports


class Command(BaseCommand):
    help = "Updates the Reports of all Contracts from all active, non-staff Users."

    def add_arguments(self, parser):
        parser.add_argument("start_month", type=int)

        parser.add_argument("start_year", type=int)
        parser.add_argument(
            "--all",
            action="store_true",
            help="Update thre Reports from all Users including non-active ones.",
        )

    def handle(self, *args, **options):
        start_month_year = datetime.date(
            options["start_year"], options["start_month"], 1
        )
        contract_qs = Contract.objects.filter(
            user__is_active=True,
            user__is_staff=False,
            start_date__gte=start_month_year,
        )
        contract_cnt = 0
        for contract in contract_qs:
            start_month_year = contract.start_date.replace(day=1)
            update_reports(contract, start_month_year)
            contract_cnt += 1

        self.stdout.write(
            self.style.SUCCESS(
                "The Reports of {} Contracts were successfully updated.".format(
                    contract_cnt
                )
            )
        )
