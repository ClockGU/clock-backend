import datetime

from django.core.management.base import BaseCommand, CommandError

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
        # TODO: optional arguments --end_month, --end_year

    def handle(self, *args, **options):
        start_month_year = datetime.date(
            options["start_year"], options["start_month"], 1
        )
        contract_qs = Contract.objects.filter(
            user__is_active=True,
            user__is_staff=False,
            start_date__lte=start_month_year,
            end_date__gte=start_month_year,
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
