"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
import json
from datetime import datetime

import pytest
from dateutil.parser import parse
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time
from rest_framework import serializers, status

from api.models import Contract, Report, Shift, User


class TestContractApiEndpoint:
    """
    This TestCase includes:
    - tests which try accesing an Endpoint without a provided JWT
        --> These tests will not be repeated for other Endpoints since in V1
            every endpoint shares the same permission_class and
            authentication_class

    - tests which try to change the values for user, created_by and modified by
        --> These tests will not be repeated for other Endpoints since in V1
            every endpoint shares the same base serializer which provides this
            provides this Functionality

    - tests which try to create a Contract for a different user than who is
    issueing the request
        --> These tests will not be repeated for other Endpoints since in V1
            every endpoint shares the same base serializer which provides this
            provides this Functionality
    """

    @pytest.mark.django_db
    def test_get_only_own_contract(
        self, client, user_object_jwt, diff_user_contract_object
    ):
        """
        Test that attempting to retrieve a contract, which does not belong to the User requesting it,
        gives a 404 response.
        :param client:
        :param user_object_jwt:
        :param diff_user_contract_object:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:contracts-detail", args=[diff_user_contract_object.id]),
            content_type="application/json",
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_forbidden_without_jwt(self, client, contract_object):
        """
        Test the detail Endpoint returns a 401 if no JWT is present.
        :param client:
        :param contract_object:
        :param user_object:
        :return:
        """
        response = client.get(
            path=r"/contracts/",
            args=[contract_object.id],
            content_type="application/json",
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_list_forbidden_without_jwt(self, client):
        """
        Test the list endpoint returns a 401 if no JWT is present.
        :param client:
        :return:
        """
        response = client.get(
            path="http://localhost:8000/contracts/", content_type="application/json"
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_create_forbidden_without_jwt(self, client, valid_contract_json):
        """
        Test the create endpoint returns a 401 if no JWT is present.
        :param client:
        :param valid_contract_json:
        :return:
        """
        response = client.post(
            path="http://localhost:8000/contracts/",
            data=json.dumps(valid_contract_json),
            content_type="application/json",
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_put_forbidden_without_jwt(self, client, valid_contract_json):
        """
        Test the PUT endpoint returns 401 if no JWT is present.
        :param client:
        :param valid_contract_json:
        :return:
        """

        response = client.put(
            path="http://localhost:8000/contracts/",
            data=json.dumps(valid_contract_json),
            content_type="application/json",
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_list_objects_of_request_user(
        self, client, user_object, user_object_jwt, db_creation_contracts_list_endpoint
    ):
        """
        Test that the list-endpoint only retrieves the Contracts of the User who issues the request.
        :param client:
        :param user_object:
        :param user_object_jwt:
        :param db_creation_contracts_list_endpoint:
        :return:
        """

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path="http://localhost:8000/contracts/", content_type="application/json"
        )
        data = json.loads(response.content)
        assert response.status_code == 200
        assert all(
            Contract.objects.get(id=contract["id"]).user.id == user_object.id
            for contract in data
        )

    @pytest.mark.freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_create_with_correct_user(
        self,
        client,
        invalid_uuid_contract_json,
        user_object,
        user_object_jwt,
        delete_report_object_afterwards,
    ):
        """
        Test that 'user', 'created_by' and 'modified_by' (incorrectly set invalid_uuid_contract_json)
        are set to the user_id from the JWT of the request.

        We include the 'delete_report_object_afterwards' since the Contract creation triggers
        a Report object creation.
        :param client:
        :param invalid_uuid_contract_json:
        :param user_object:
        :param user_object_jwt:
        :return:
        """

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path="/contracts/",
            data=json.dumps(invalid_uuid_contract_json),
            content_type="application/json",
        )

        content = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        new_contract = Contract.objects.get(id=content["id"])

        assert new_contract.user.id == user_object.id
        assert new_contract.created_by.id == user_object.id
        assert new_contract.created_by.id == user_object.id

    @pytest.mark.freeze_time("2019-01-10 00:05:00")
    @pytest.mark.django_db
    def test_update_uuid_contract(
        self,
        client,
        invalid_uuid_contract_put_endpoint,
        contract_object,
        user_object,
        user_object_jwt,
        freezer,
    ):
        """
        Test that updating 'user', 'created_by' and 'modified_by' does not work.
        This is tested via 'invalid_uuid_contract_json' which has non-existent uuid's in these fields.
        By testing with this fixture it is also covered that even if the uuid corresponds to an existent user
        it is not possible to switch/modify the contracts owner.

        :param client:
        :param invalid_uuid_contract_put_endpoint:
        :param contract_object:
        :return:
        """
        freezer.move_to(
            "2019-01-10 00:07:00"
        )  # can't shift to far because the JWT might expire (~5min)
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:contracts-detail", args=[contract_object.id]),
            data=json.dumps(invalid_uuid_contract_put_endpoint),
            content_type="application/json",
        )
        content = json.loads(response.content)
        print(content)
        assert response.status_code == 200
        # Check that neither "user", "created_by" nor "modified_by" changed from the originial/issuing user
        user_id = user_object.id
        contract = Contract.objects.get(id=contract_object.id)
        assert contract.user.id == user_id
        assert contract.created_by.id == user_id
        assert contract.modified_by.id == user_id
        #      New Datetime           Old Datetime  --> Result should be positive
        assert contract.modified_at > contract_object.modified_at

    @pytest.mark.freeze_time("2019-01-10 00:05:00")
    @pytest.mark.django_db
    def test_patch_uuid_contract(
        self,
        client,
        invalid_uuid_contract_patch_endpoint,
        contract_object,
        user_object,
        user_object_jwt,
        freezer,
    ):
        """
        Test that trying to patch 'user, 'created_by' and 'mdofied_by' does not work.
        Updating other values do not need to be tested here.
        :param client:
        :param invalid_uuid_contract_patch_endpoint:
        :param contract_object:
        :param user_object:
        :param user_object_jwt:
        :return:
        """
        freezer.move_to(
            "2019-01-10 00:07:00"
        )  # can't shift to far because the JWT might expire (~5min)
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.patch(
            path=reverse("api:contracts-detail", args=[contract_object.id]),
            data=json.dumps(invalid_uuid_contract_patch_endpoint),
            content_type="application/json",
        )
        contract = Contract.objects.get(id=contract_object.id)
        user_id = user_object.id
        assert response.status_code == 200

        assert contract.user.id == user_id
        assert contract.created_by.id == user_id
        assert contract.modified_by.id == user_id
        # Due to freeze_time not testable anymore...
        # No clue how to change this.
        #      New Datetime           Old Datetime  --> Result should be positive
        # assert contract.modified_at > contract_object.modified_at

    @pytest.mark.django_db
    def test_shifts_action_contract(
        self,
        client,
        user_object_jwt,
        user_object,
        contract_object,
        db_creation_shifts_list_endpoint,
    ):
        """
        Test that the endpoint contracts/<uuid>/shifts exists and that it lists all shifts
        corresponding to the contract with <uuid>.
        :param client:
        :param user_object_jwt:
        :param user_object:
        :param contract_object:
        :param db_creation_shifts_list_endpoint:
        :return:
        """

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:contracts-shifts", args=[contract_object.id]),
            content_type="application/json",
        )

        content = json.loads(response.content)

        assert len(content) == 2  # We created only 2 shifts for the User
        assert all(shift["contract"] == str(contract_object.id) for shift in content)

    @pytest.mark.freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_automatic_report_creation_upon_contract_creation(
        self,
        client,
        valid_contract_json,
        user_object,
        user_object_jwt,
        contract_object,
        delete_report_object_afterwards,
    ):
        """
        Test that after the creation of a valid Contract a Report for it's start month is created
        for the User which creates the contract.
        :param client:
        :param valid_contract_json:
        :param user_object:
        :param user_object_jwt:
        :param contract_object:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path="/contracts/",
            data=json.dumps(valid_contract_json),
            content_type="application/json",
        )

        content = json.loads(response.content)
        start_date = (
            datetime.strptime(content["start_date"], "%Y-%m-%d").replace(day=1).date()
        )
        assert Report.objects.get(
            user=user_object, month_year=start_date, contract=contract_object
        )

    @pytest.mark.django_db
    def test_locking_shifts(
        self,
        client,
        contract_object,
        shift_object,
        user_object_jwt,
        mock_api,
        aggregated_report_data,
    ):
        mock_api.post(
            f"{settings.TIME_VAULT_URL}/reports/",
            json=aggregated_report_data,
            status_code=201,
        )
        assert not shift_object.locked
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path=reverse(
                "api:contracts-lock-shifts",
                args=[
                    str(contract_object.id),
                    shift_object.started.month,
                    shift_object.started.year,
                ],
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert Shift.objects.get(pk=shift_object.pk).locked

    @pytest.mark.django_db
    def test_locking_shifts_without_personal_number(
        self, client, contract_object, shift_object, user_object_jwt, user_object
    ):
        user_object.personal_number = ""
        user_object.save()
        assert not shift_object.locked
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path=reverse(
                "api:contracts-lock-shifts",
                args=[
                    str(contract_object.id),
                    shift_object.started.month,
                    shift_object.started.year,
                ],
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert not Shift.objects.get(pk=shift_object.pk).locked

    @pytest.mark.django_db
    def test_queryset_ordering(
        self,
        user_object,
        create_n_contract_objects,
        freezer,
        prepared_ContractViewSet_view,
    ):
        freezer.move_to(datetime(2019, 1, 1, 1))
        for i in range(2, 6):
            create_n_contract_objects((1,), user_object)
            freezer.move_to(datetime(2019, 1, 1, i))
        qs = prepared_ContractViewSet_view.get_queryset()
        # Check a) ordering b) ascending
        assert qs.ordered
        assert all(qs[i].last_used > qs[i + 1].last_used for i in range(len(qs) - 1))


class TestShiftApiEndpoint:
    @pytest.mark.django_db
    def test_list_objects_of_request_user(
        self, client, user_object, user_object_jwt, db_creation_shifts_list_endpoint
    ):
        """
        Test that the list-endpoint only retrieves the Shifts of the User who issues the request.
        :param client:
        :param user_object:
        :param user_object_jwt:
        :param db_creation_shifts_list_endpoint:
        :return:
        """

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:shifts-list"), content_type="application/json"
        )

        data = json.loads(response.content)
        assert response.status_code == 200
        assert all(
            Shift.objects.get(id=shift["id"]).user.id == user_object.id
            for shift in data
        )

    @pytest.mark.django_db
    def test_create(self, client, user_object, user_object_jwt, valid_shift_json):
        """
        Test that the create-endpoint creates the Shift correctly. Special focus on valid creation of the
        provided tags.
        :param client:
        :param user_object:
        :param user_object_jwt:
        :param valid_shift_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path=reverse("api:shifts-list"),
            data=json.dumps(valid_shift_json),
            content_type="application/json",
        )
        data = json.loads(response.content)

        assert response.status_code == 201
        shift_object = Shift.objects.get(pk=data["id"])
        initial_tags = valid_shift_json["tags"]

        assert shift_object
        assert shift_object.tags.all().count() == len(initial_tags)

        assert all(
            shift_tag.name in initial_tags for shift_tag in shift_object.tags.all()
        )

    @pytest.mark.django_db
    def test_put_new_tags(self, client, user_object_jwt, put_new_tags_json):
        """
        Test that the PUT-endpoint updates the tags correctly.
        :param client:
        :param user_object_jwt:
        :param put_new_tags_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:shifts-detail", args=[put_new_tags_json["id"]]),
            data=json.dumps(put_new_tags_json),
            content_type="application/json",
        )
        data = json.loads(response.content)
        print(data)
        assert response.status_code == 200
        initial_tags = put_new_tags_json["tags"]
        shift_object = Shift.objects.get(pk=data["id"])
        assert shift_object.tags.all().count() == len(initial_tags)
        assert all(
            shift_tag.name in initial_tags for shift_tag in shift_object.tags.all()
        )

    @pytest.mark.django_db
    def test_patch_new_tags(self, client, user_object_jwt, patch_new_tags_json):
        """
        Test that the PATCH-endpoint updates the Tags correctly.
        Here it is worth noteing that all Tags, even those who are kept, are needed within the payload.
        :param client:
        :param user_object_jwt:
        :param patch_new_tags_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.patch(
            path=reverse("api:shifts-detail", args=[patch_new_tags_json["id"]]),
            data=json.dumps(patch_new_tags_json),
            content_type="application/json",
        )

        initial_tags = patch_new_tags_json["tags"]

        assert response.status_code == 200
        shift_object = Shift.objects.get(pk=patch_new_tags_json["id"])

        assert shift_object.tags.all().count() == len(initial_tags)
        assert all(
            shift_tag.name in initial_tags for shift_tag in shift_object.tags.all()
        )

    @pytest.mark.django_db
    def test_patch_empty_tags(self, client, user_object_jwt, patch_empty_tags_json):
        """
        Test that the PATCH-endpoint updates the Tags correctly.
        Here it is worth noteing that all Tags, even those who are kept, are needed within the payload.
        :param client:
        :param user_object_jwt:
        :param patch_new_tags_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.patch(
            path=reverse("api:shifts-detail", args=[patch_empty_tags_json["id"]]),
            data=json.dumps(patch_empty_tags_json),
            content_type="application/json",
        )

        assert response.status_code == 200
        shift_object = Shift.objects.get(pk=patch_empty_tags_json["id"])

        assert shift_object.tags.all().count() == 0

    @pytest.mark.django_db
    @pytest.mark.freeze_time(
        "2019-02-10"
    )  # needed for fixture creation --> Report creation signal on Contract creation
    def test_list_month_year_endpoint(
        self, client, user_object_jwt, db_creation_list_month_year_endpoint
    ):
        """
        Test that the endpoint list-shifts/<month>/<year>/ exists and that it lists all Shifts
        of the provided <month> in the provided <year> corresponding to the User issueing the request.
        :param client:
        :param user_object_jwt:
        :param db_creation_list_month_year_endpoint:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:list-shifts", args=[1, 2019]),
            content_type="application/json",
        )

        data = json.loads(response.content)

        assert response.status_code == 200
        assert len(data) == 2
        assert all(
            parse(i["started"]).month == 1 and parse(i["started"]).year == 2019
            for i in data
        )

    @pytest.mark.django_db
    def test_updating_exported_shift_returns_403(
        self, client, user_object_jwt, put_to_exported_shift_json
    ):
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:shifts-detail", args=[put_to_exported_shift_json["id"]]),
            data=json.dumps(put_to_exported_shift_json),
            content_type="application/json",
        )
        print(json.loads(response.content))
        assert response.status_code == 403


class TestClockedInShiftEndpoint:
    @pytest.mark.django_db
    def test_get_endpoint_without_pk(
        self, client, user_object_jwt, clockedinshift_object
    ):
        """
        Test that the endpoint clockedinshifts/ returns a detail representation of the only existing
        ClockedInShift object.
        :param client:
        :param user_object_jwt:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(path="/clockedinshifts/", content_type="application/json")
        content = json.loads(response.content)
        assert content["id"] == str(clockedinshift_object.id)

    @pytest.mark.django_db
    def test_get_endpoint_returns_404(self, client, user_object_jwt):
        """
        Test that the endpoint clockedinshifts/ returns a 404 status if no
        ClockedInShift object exists.
        :param client:
        :param user_object_jwt:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(path="/clockedinshifts/", content_type="application/json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_creating_second_obeject_not_allowed(
        self, client, user_object_jwt, clockedinshift_object, valid_clockedinshift_json
    ):
        """
        Test that the attempt of creating a second ClockedInShift object results in a 400 Response.
        :param client:
        :param user_object_jwt:
        :param clockedinshift_object:
        :param valid_clockedinshift_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.post(
            path="/clockedinshifts/",
            data=json.dumps(valid_clockedinshift_json),
            content_type="application/json",
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_put_action_allowed(
        self, client, user_object_jwt, clockedinshift_object, update_clockedinshift_json
    ):
        """
        Test that the attempt of creating a second ClockedInShift object results in a 400 Response.
        :param client:
        :param user_object_jwt:
        :param clockedinshift_object:
        :param valid_clockedinshift_json:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:clockedinshifts-detail", args=[clockedinshift_object.id]),
            data=json.dumps(update_clockedinshift_json),
            content_type="application/json",
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_patch_action_allowed(
        self, client, user_object_jwt, clockedinshift_object, update_clockedinshift_json
    ):
        """
        Test that the attempt of creating a second ClockedInShift object results in a 400 Response.
        :param client:
        :param user_object_jwt:
        :param clockedinshift_object:
        :param valid_clockedinshift_json:
        :return:
        """
        update_clockedinshift_json["id"] = str(clockedinshift_object.id)
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.patch(
            path=reverse("api:clockedinshifts-detail", args=[clockedinshift_object.id]),
            data=json.dumps(update_clockedinshift_json),
            content_type="application/json",
        )
        assert response.status_code == 200


class TestReportApiEndpoint:
    @pytest.mark.freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_get_current_endpoint(
        self, client, user_object_jwt, db_get_current_endpoint, contract_object
    ):
        """
        Test that the endpoint reports/get_current/ exists and that it retrieves the Report for the current
        month.
        :param client:
        :param user_object_jwt:
        :param db_get_current_endpoint:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:reports-get_current", args=[contract_object.id]),
            content_type="application/json",
        )
        content = json.loads(response.content)
        assert content["month_year"] == "2019-01-01"

    @pytest.mark.django_db
    def test_aggregate_shift_content_method_retrieves_all_shifts(
        self,
        prepared_ReportViewSet_view,
        shift_content_aggregation_gather_all_shifts,
        report_object,
    ):
        """
        Test that the utility method of the ReportViewSet 'aggregate_shift_content' catches all Shifts of a month.
        :return:
        """
        content = prepared_ReportViewSet_view.aggregate_days_content(
            shift_content_aggregation_gather_all_shifts
        )

        assert len(content) == 5

    @pytest.mark.django_db
    def test_aggregate_shift_content_method_omits_planned_shifts(
        self,
        prepared_ReportViewSet_view,
        shift_content_aggregation_ignores_planned_shifts,
        report_object,
    ):
        """
        Test that the utility method of the ReportViewSet 'aggregate_shift_content' catches all Shifts of a month
        but omits planned Shifts.

        The Fixture provides 5 Shifts as the 'shift_content_aggregation_gather_all_shifts' fixture and an additional
        Shift which is planned (was_reviewed=False).
        :param prepared_ReportViewSet_view:
        :param shift_content_aggregation_ignores_planned_shifts:
        :param report_objects:
        :return:
        """
        content = prepared_ReportViewSet_view.get_shifts_to_export(report_object)

        assert len(content) == 5

    @pytest.mark.django_db
    def test_aggregate_shift_content_merges_multiple_shifts(
        self,
        prepared_ReportViewSet_view,
        shift_content_aggregation_merges_shifts,
        report_object,
    ):
        content = prepared_ReportViewSet_view.aggregate_days_content(
            shift_content_aggregation_merges_shifts
        )

        assert len(content) == 1
        assert content["26.01.2019"]
        assert content["26.01.2019"]["started"] == "10:00"
        assert content["26.01.2019"]["stopped"] == "18:00"
        assert content["26.01.2019"]["worktime"] == "06:00"
        assert content["26.01.2019"]["breaktime"] == "02:00"

    @pytest.mark.django_db
    def test_aggregate_shift_content_handles_vacation_shifts(
        self, prepared_ReportViewSet_view, two_vacation_shifts
    ):
        content = prepared_ReportViewSet_view.aggregate_days_content(
            two_vacation_shifts
        )

        assert len(content) == 1
        assert content["26.01.2019"]
        assert content["26.01.2019"]["started"] == "10:00"
        assert content["26.01.2019"]["stopped"] == "18:00"
        assert content["26.01.2019"]["breaktime"] == "00:30"
        assert content["26.01.2019"]["worktime"] == "07:30"
        assert content["26.01.2019"]["type"] == _("Vacation")
        assert content["26.01.2019"]["absence_type"] == "U"

    @pytest.mark.freeze_time("2019-02-10")
    @pytest.mark.django_db
    def test_general_content_debit_worktime_mid_month(
        self, prepared_ReportViewSet_view_mid_january, contract_start_mid_january
    ):
        """
        Test wether the debit_worktime of the general_content is correct for start/end months of a contract
        whcih start/end in the middle.
        :param prepared_ReportViewSet_view_mid_january:
        :return:
        """
        rep = contract_start_mid_january.reports.get(
            month_year=contract_start_mid_january.start_date.replace(day=1)
        )
        content = prepared_ReportViewSet_view_mid_january.aggregate_general_content(
            rep, None
        )

        assert content["debit_worktime"] == "10:19"

    @pytest.mark.django_db
    def test_compile_pdf_returns_pdf(self, prepared_ReportViewSet_view, report_object):
        """
        Test whether the method actually returns a PDF file.
        :param prepared_ReportViewSet_view:
        :return:
        """
        export_content = prepared_ReportViewSet_view.aggregate_export_content(
            report_object
        )

        pdf = prepared_ReportViewSet_view.compile_pdf(
            template_name="api/stundenzettel.html", content_dict=export_content
        )
        assert pdf.startswith(bytes("%PDF-1", "UTF-8"))

    @pytest.mark.django_db
    def test_export_endpoint_returns_file(self, report_object, client, user_object_jwt):
        """
        Test that the Endpoint really returns a file.
        :param report_object:
        :param client:
        :param user_object_jwt:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path=reverse("api:reports-export", args=[report_object.pk])
        )

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_export_endpoint_validates_overlapping_shifts(
        self, prepared_ReportViewSet_view, overlapping_shifts
    ):
        """

        :param prepared_ReportViewSet_view:
        :param overlapping_shifts:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            prepared_ReportViewSet_view.check_for_overlapping_shifts(overlapping_shifts)

    @pytest.mark.django_db
    def test_export_endpoint_validates_not_locked_shifts(
        self,
        prepared_ReportViewSet_view,
        second_months_report_locked_shifts,
        not_locked_shifts,
    ):
        """
        The provided Report belongs to a Contract which has unlocked, not planned shifts in the
        first month. The check_for_not_locked_shifts() Method should hence throw an ValidationError.
        """
        with pytest.raises(serializers.ValidationError):
            prepared_ReportViewSet_view.check_for_not_locked_shifts(
                second_months_report_locked_shifts
            )

    @pytest.mark.django_db
    def test_export_marks_violations(
        self, prepared_ReportViewSet_view, eleven_hour_shift, report_object
    ):
        shifts = prepared_ReportViewSet_view.get_shifts_to_export(report_object)
        aggregated_shift_content = prepared_ReportViewSet_view.aggregate_days_content(
            shifts
        )

        assert aggregated_shift_content["29.01.2019"]["notes"] == "1, 5"


class TestDjoserCustomizing:
    @pytest.mark.django_db
    def test_delete_user_custom_serializer(self, user_object, user_object_jwt, client):
        """
        Test if the user-delete view works with the specified custom UserSerializer.
        :param user_object:
        :param user_object_jwt:
        :param client:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.delete(path=reverse("user-me"))
        assert response.status_code == 204
        assert not User.objects.filter(id=user_object.id).exists()

    @pytest.mark.django_db
    def test_put_user_custom_serializer(
        self, user_object, user_object_jwt, user_object_json, client
    ):
        """
        Test if the user/me/ PUT view works with the specified custom UserSerializer.
        :param user_object:
        :param user_object_jwt:
        :param client:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        put_data = user_object_json
        put_data["language"] = "de"
        put_data["personal_number"] = "66666666"
        response = client.put(
            path=reverse("user-me"),
            data=json.dumps(put_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert User.objects.get(id=user_object.id).language == "de"
        assert User.objects.get(id=user_object.id).personal_number == "66666666"

    @pytest.mark.django_db
    def test_patch_user_custom_serializer(self, user_object, user_object_jwt, client):
        """
        Test if the user/me/ PATCH view works with the specified custom UserSerializer.
        :param user_object:
        :param user_object_jwt:
        :param client:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        put_data = {"language": "de", "personal_number": "66666666"}
        response = client.patch(
            path=reverse("user-me"),
            data=json.dumps(put_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert User.objects.get(id=user_object.id).language == "de"
        assert User.objects.get(id=user_object.id).personal_number == "66666666"
