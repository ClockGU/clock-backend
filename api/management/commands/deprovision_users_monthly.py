from __future__ import absolute_import

from api.idm.deprovisioning import Deprovisioner


def deprovision_users_monthly(self):
    """
    This is a Periodical task which runs the deprovision.
    """
    Deprovisioner().deprovision()
