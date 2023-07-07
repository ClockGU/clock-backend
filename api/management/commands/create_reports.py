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

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError

from api.models import Report, User


class Command(BaseCommand):
    help = "Create missing Reports for all Users for the given month and year."

    def add_arguments(self, parser):
        parser.add_argument("month", type=int)

        parser.add_argument("year", type=int)

    def handle(self, *args, **options):
        report_cnt = 0
        date = datetime.date(options["year"], options["month"], 1)

        if date >= datetime.date.today():
            raise CommandError("It's not allowed to create Reports for future months.")

        for user in User.objects.filter(is_active=True, is_staff=False):
            for contract in user.contracts.filter(
                start_date__lt=date, end_date__gt=date
            ).exclude(reports__month_year=date):
                last_report = Report.objects.get(
                    contract=contract, month_year=date - relativedelta(months=1)
                )
                carry_over_worktime = datetime.timedelta(0)

                if last_report:
                    carry_over_worktime = last_report.worktime - datetime.timedelta(
                        minutes=contract.minutes
                    )

                Report.objects.create(
                    month_year=date,
                    worktime=carry_over_worktime,
                    contract=contract,
                    user=user,
                    created_by=user,
                    modified_by=user,
                )
                report_cnt += 1

        self.stdout.write(
            self.style.SUCCESS("{} Reports were created.".format(report_cnt))
        )
