from __future__ import absolute_import

from api.idm.deprovisioning import Deprovisioner
from project_celery.celery import app


@app.task(bind=True, default_retry_delay=10)
def deprovision_users_monthly(self):
    """
    This is a Periodical task which runs the deprovision.
    """
    Deprovisioner().deprovision()
