from django.core.management.base import BaseCommand, CommandError
from api.models import User, Contract, Report
import datetime
from dateutil.relativedelta import relativedelta


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
                carry_over_minutes = datetime.timedelta(0)

                if last_report:
                    carry_over_minutes = last_report.minutes - datetime.timedelta(
                        minutes=contract.minutes
                    )

                Report.objects.create(
                    month_year=date,
                    minutes=carry_over_minutes,
                    contract=contract,
                    user=user,
                    created_by=user,
                    modified_by=user,
                )
                report_cnt += 1

        self.stdout.write(
            self.style.SUCCESS("{} Reports were created.".format(report_cnt))
        )
