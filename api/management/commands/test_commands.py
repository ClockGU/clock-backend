from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
import pytest


class TestCreateReportsCommand:
    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_no_report_created_if_report_exists(self, contract_object):
        """
        Test if the command skips the creation of a Report in the specified month if one already exists.
        It's tested here with a Contract that only last for one month and hence got the Report created on
        Contract creation.

        :param contract_object:
        :return:
        """
        out = StringIO()
        call_command("create_reports", "1", "2019", stdout=out)

        assert "0 Reports were created." in out.getvalue()

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_created_report_successful(self, contract_ending_in_february, freezer):
        """
        Test that the command actually creates a Report.
        :param contract_ending_in_february:
        :param freezer:
        :return:
        """
        freezer.move_to("2019-02-02")
        out = StringIO()
        call_command("create_reports", "2", "2019", stdout=out)

        assert "1 Reports were created." in out.getvalue()

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_created_report_fails_for_future_dates(self, contract_object):
        """
        Test that the command does not allow creation of reports in the future.
        :param contract_object:
        :return:
        """
        out = StringIO()
        with pytest.raises(CommandError) as e_info:
            call_command("create_reports", "2", "2019", stdout=out)
