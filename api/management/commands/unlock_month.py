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

        shifts = Shift.objects.filter(user=user, started__month=options["month"], started__year=options["year"])
        shifts.update(locked=False)
        self.stdout.write(
            self.style.SUCCESS(f"All Shifts in {options['month']}.{options['year']} (MM.YYYY) are unlocked.")
        )
