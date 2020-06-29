import pytest
from pytz import datetime

from api.models import Report

# This conftest file provides all necessary test data concerning the Report Model.
# It will be imported by the conftest.py in the parent directory.


@pytest.fixture
def create_n_report_objects():
    """
    This fixture resembles a report object factory.
    Shifts are distinguised by id, there is no specific need for the start_stop mechanism.
    Nonetheless in terms of consistency this mechanism is kept as in the user_conftest.py.
    :return: Function
    """
    month_year = datetime.date(2019, 1, 1)
    _minutes = datetime.timedelta(0)
    created_at = datetime.datetime(2019, 1, 1, 16).isoformat()
    modified_at = created_at

    def create_reports(
        start_stop, user, contract, minutes=_minutes, month_year=month_year
    ):
        lst = []
        for i in range(*start_stop):
            report = Report.objects.create(
                month_year=month_year,
                minutes=minutes,
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
    """
    This fixture creates one report object for January.
    :param create_n_report_objects:
    :param user_object:
    :param contract_object:
    :return:
    """
    # Clear all previously created Reports which might have been created
    Report.objects.all().delete()
    return create_n_report_objects((1,), user_object, contract_object)[0]


@pytest.fixture
def report_update_february_report(
    create_n_report_objects, report_update_user, report_update_contract
):
    return create_n_report_objects(
        (1,),
        report_update_user,
        report_update_contract,
        minutes=datetime.timedelta(minutes=-1200),
        month_year=datetime.date(2019, 2, 1),
    )[0]


@pytest.fixture
def previous_report_object(create_n_report_objects, user_object, contract_object):
    """
    This fixture creates a report object for preceeding report_object with a
    carry_over of 120 minutes
    :param create_n_report_objects: :param user_object: :param contract_object:
    :return:
    """
    return create_n_report_objects(
        (1,),
        user_object,
        contract_object,
        minutes=datetime.timedelta(minutes=1320),
        month_year=datetime.date(2018, 12, 1),
    )[0]


@pytest.fixture
def january_report_object(
    create_n_report_objects, user_object, contract_ending_in_february
):
    """
    This fixture creates one report object for February.
    :param create_n_report_objects:
    :param user_object:
    :param contract_ending_in_february:
    :return:
    """

    return create_n_report_objects(
        (1,),
        user_object,
        contract_ending_in_february,
        minutes=datetime.timedelta(minutes=1320),
        month_year=datetime.date(2019, 1, 1),
    )[0]


@pytest.fixture
def february_report_object(
    create_n_report_objects, user_object, contract_ending_in_february
):
    """
    This fixture creates one report object for February.
    :param create_n_report_objects:
    :param user_object:
    :param contract_ending_in_february:
    :return:
    """
    return create_n_report_objects(
        (1,),
        user_object,
        contract_ending_in_february,
        month_year=datetime.date(2019, 2, 1),
    )[0]


@pytest.fixture
def delete_report_object_afterwards():

    yield
    Report.objects.all().delete()


@pytest.fixture
def db_get_current_endpoint(
    create_n_report_objects, user_object, contract_object, report_object
):
    """
    This fixture creates two reports for February and March 2019.
    :param create_n_report_objects:
    :param user_object:
    :param contract_object:
    :param report_object:
    :return:
    """
    # create 2 more Reports for February and March
    create_n_report_objects(
        (1,), user_object, contract_object, month_year=datetime.date(2019, 2, 1)
    )
    create_n_report_objects(
        (1,), user_object, contract_object, month_year=datetime.date(2019, 3, 1)
    )


@pytest.fixture
def second_months_report_locked_shifts(contract_locked_shifts):
    """
    This fixture retrieves the Report object of the second month of the provided contract.
    """
    return Report.objects.get(
        contract=contract_locked_shifts, month_year=datetime.date(2020, 2, 1)
    )
