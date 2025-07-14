import datetime

import pytest

from .shift_conftest import create_n_shift_objects
from .contract_conftest import create_n_contract_objects
from .user_conftest import user_object
from ...models import Report


@pytest.fixture
def report_carryover_account_contract(create_n_contract_objects, user_object):
    """
    Creates a contract from 1.1.2019 - 31.3.2019
    with debit worktime of 20 hours and an initial carryover of 2460 minutes (41 hours).
    """
    contract = create_n_contract_objects(
        (1,),
        initial_carryover_minutes=2460,
        user=user_object,
        end_date=datetime.date(2019,3,31)
    )[0]
    return contract

@pytest.fixture
@pytest.mark.django_db
def january_report_initial_carryover_account(report_carryover_account_contract):
    """
    Creates a contract from 1.1.2019 - 31.3.2019
    with debit worktime of 20 hours and an initial carryover of 2460 minutes (41 hours).
    """
    return Report.objects.get(contract=report_carryover_account_contract, month_year=datetime.date(2019, 1, 1))

@pytest.fixture
@pytest.mark.django_db
def february_report_initial_carryover_account(report_carryover_account_contract):
    """
    Creates a contract from 1.1.2019 - 31.3.2019
    with debit worktime of 20 hours and an initial carryover of 2460 minutes (41 hours).
    """
    return Report.objects.get(contract=report_carryover_account_contract, month_year=datetime.date(2019, 2, 1))


@pytest.fixture
def report_initial_carryover_with_shifts_account(january_report_initial_carryover_account, create_n_shift_objects):
    """
    Creates two 5 hour shifts on 3. and 4. January 2019.
    """

    contract = january_report_initial_carryover_account.contract
    user = january_report_initial_carryover_account.user
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,3,10),
        stopped=datetime.datetime(2019,1,3,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,4,10),
        stopped=datetime.datetime(2019,1,4,15)
    )
    return january_report_initial_carryover_account

@pytest.fixture
def report_carryover_with_additional_overtime(january_report_initial_carryover_account, create_n_shift_objects):
    """
    Creates five 5 hour shifts on 3., 4., 5., 6., 7. January 2019.
    """
    contract = january_report_initial_carryover_account.contract
    user = january_report_initial_carryover_account.user
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,3,10),
        stopped=datetime.datetime(2019,1,3,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,4,10),
        stopped=datetime.datetime(2019,1,4,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,5,10),
        stopped=datetime.datetime(2019,1,5,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,6,10),
        stopped=datetime.datetime(2019,1,6,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,7,10),
        stopped=datetime.datetime(2019,1,7,15)
    )
    return january_report_initial_carryover_account

@pytest.fixture
def report_carryover_with_too_much_additional_overtime(january_report_initial_carryover_account, create_n_shift_objects):
    """
    Creates seven 5 hour shifts on 3., 4., 5., 6., 7., 8., 9. January 2019.
    """
    contract = january_report_initial_carryover_account.contract
    user = january_report_initial_carryover_account.user
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,3,10),
        stopped=datetime.datetime(2019,1,3,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,4,10),
        stopped=datetime.datetime(2019,1,4,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,5,10),
        stopped=datetime.datetime(2019,1,5,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,6,10),
        stopped=datetime.datetime(2019,1,6,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,7,10),
        stopped=datetime.datetime(2019,1,7,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,8,10),
        stopped=datetime.datetime(2019,1,8,15)
    )
    create_n_shift_objects(
        (1,),
        user,
        contract,
        started=datetime.datetime(2019,1,9,10),
        stopped=datetime.datetime(2019,1,9,15)
    )
    return january_report_initial_carryover_account
