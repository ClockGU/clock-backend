from __future__ import absolute_import

from typing import Any

from django.core.management.base import BaseCommand

from api.idm.deprovisioning import Deprovisioner


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        deprovision_users_monthly()

def deprovision_users_monthly():
    """
    This is a Periodical task which runs the deprovision.
    """
    Deprovisioner().deprovision()
