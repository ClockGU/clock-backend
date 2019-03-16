import pytest
from pytz import datetime

from api.models import Report


@pytest.fixture
def create_n_report_objects():
    month_year = datetime.date(2019, 1, 1)
    hours = datetime.timedelta(0)
    created_at = datetime.datetime(2019, 1, 1, 16).isoformat()
    modified_at = created_at

    def create_reports(start_stop, user, contract, month_year=month_year):
        lst = []
        for i in range(*start_stop):
            report = Report.objects.create(
                month_year=month_year,
                hours=hours,
                contract=contract,
                user=user,
                created_by=user,
                modified_by=user,
                created_at=created_at,
                modified_at=modified_at,
            )
            lst.append(report)

        return lst

    return create_reports


@pytest.fixture
def report_object(create_n_report_objects, user_object, contract_object):
    return create_n_report_objects((1,), user_object, contract_object)[0]


@pytest.fixture
def db_get_current_endpoint(
    create_n_report_objects, user_object, contract_object, report_object
):
    # create 2 more Reports for February and March
    create_n_report_objects(
        (1,), user_object, contract_object, month_year=datetime.date(2019, 2, 1)
    )
    create_n_report_objects(
        (1,), user_object, contract_object, month_year=datetime.date(2019, 3, 1)
    )
