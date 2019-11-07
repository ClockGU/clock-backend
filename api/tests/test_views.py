# View tests come here

import json
from datetime import datetime
from dateutil.parser import parse

import pytest
import time
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status, serializers

from api.models import Contract, Shift, Report


class TestContractApiEndpoint:
    """
    This TestCase includes:
       - tests which try accesing an Endpoint without a provided JWT
           --> These tests will not be repeated for other Endpoints since in V1 every endpoint shares the same
               permission_class and authentication_class
       - tests which try to change the values for user, created_by and modified by
           --> These tests will not be repeated for other Endpoints since in V1 every endpoint shares the same base
               serializer which provides this provides this Functionality
       - tests which try to create a Contract for a different user than who is issueing the request
           --> These tests will not be repeated for other Endpoints since in V1 every endpoint shares the same base
               serializer which provides this provides this Functionality
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
            path=r"/api/contracts/",
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
            path="http://localhost:8000/api/contracts/", content_type="application/json"
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
            path="http://localhost:8000/api/contracts/",
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
            path="http://localhost:8000/api/contracts/",
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
            path="http://localhost:8000/api/contracts/", content_type="application/json"
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
            path="/api/contracts/",
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
        Test that the endpoint api/contracts/<uuid>/shifts exists and that it lists all shifts
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
            path="/api/contracts/",
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
    @pytest.mark.freeze_time(
        "2019-02-10"
    )  # needed for fixture creation --> Report creation signal on Contract creation
    def test_list_month_year_endpoint(
        self, client, user_object_jwt, db_creation_list_month_year_endpoint
    ):
        """
        Test that the endpoint api/list-shifts/<month>/<year>/ exists and that it lists all Shifts
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
        Test that the endpoint api/clockedinshifts/ returns a detail representation of the only existing
        ClockedInShift object.
        :param client:
        :param user_object_jwt:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path="/api/clockedinshifts/", content_type="application/json"
        )
        content = json.loads(response.content)
        assert content["id"] == str(clockedinshift_object.id)

    @pytest.mark.django_db
    def test_get_endpoint_returns_404(self, client, user_object_jwt):
        """
        Test that the endpoint api/clockedinshifts/ returns a 404 status if no
        ClockedInShift object exists.
        :param client:
        :param user_object_jwt:
        :return:
        """
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(
            path="/api/clockedinshifts/", content_type="application/json"
        )
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
            path="/api/clockedinshifts/",
            data=json.dumps(valid_clockedinshift_json),
            content_type="application/json",
        )
        assert response.status_code == 400


class TestReportApiEndpoint:
    @freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_get_current_endpoint(
        self, client, user_object_jwt, db_get_current_endpoint, contract_object
    ):
        """
        Test that the endpoint api/reports/get_current/ exists and that it retrieves the Report for the current
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
        content = prepared_ReportViewSet_view.aggregate_shift_content(
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

        content = prepared_ReportViewSet_view.aggregate_shift_content(
            shift_content_aggregation_merges_shifts
        )

        assert len(content) == 1
        assert content["26.01.2019"]
        assert content["26.01.2019"]["started"] == "10:00:00"
        assert content["26.01.2019"]["stopped"] == "18:00:00"
        assert content["26.01.2019"]["work_time"] == "8:00:00"
        assert content["26.01.2019"]["net_work_time"] == "6:00:00"
        assert content["26.01.2019"]["break_time"] == "2:00:00"

    @pytest.mark.django_db
    def test_aggregate_shift_content_handles_vacation_shifts(
        self, prepared_ReportViewSet_view, two_shifts_with_one_vacation_shift
    ):
        content = prepared_ReportViewSet_view.aggregate_shift_content(
            two_shifts_with_one_vacation_shift
        )

        assert len(content) == 1
        assert content["26.01.2019"]["break_time"] == "0:00:00"
        assert content["26.01.2019"]["work_time"] == "8:00:00"
        assert content["26.01.2019"]["net_work_time"] == "4:00:00"
        assert content["26.01.2019"]["type"] == "Vacation"
        assert content["26.01.2019"]["sick_or_vac_time"] == "4:00:00"

    @pytest.mark.django_db
    def test_method_to_set_shifts_exported(
        self,
        prepared_ReportViewSet_view,
        shift_content_aggregation_gather_all_shifts,
        report_object,
    ):
        """
        Test of the set_shifts_as_exported_method.

        :param prepared_ReportViewSet_view:
        :param shift_content_aggregation_gather_all_shifts:
        :param report_object:
        :return:
        """
        prepared_ReportViewSet_view.set_shifts_as_exported(report_object)

        shifts = Shift.objects.filter(
            user=report_object.user,
            contract=report_object.contract,
            started__month=1,
            started__year=2019,
        ).order_by("started")

        assert all(s.was_exported for s in shifts)

    @pytest.mark.django_db
    def test_method_for_carryover_hours_previous_month_defualt(
        self, prepared_ReportViewSet_view, report_object
    ):
        """
        Test if the method returns '00:00:00' for the carry over hours
        of the previous month if no report exists there.
        :param prepared_ReportViewSet_view:
        :param report_object:
        :return:
        """

        carry_over_hours = prepared_ReportViewSet_view.calculate_carry_over_hours(
            report_object, next_month=False
        )
        assert carry_over_hours == "00:00:00"

    @pytest.mark.django_db
    def test_method_for_carry_over_hours_previous_month(
        self, prepared_ReportViewSet_view, report_object, previous_report_object
    ):
        """
        Test if the Method calculates the hours to carry over from
        the previous moth correctly.
        :param prepared_reportViewSet_view:
        :param report_object:
        :param previous_report_object:
        :return:
        """
        carry_over_hours = prepared_ReportViewSet_view.calculate_carry_over_hours(
            report_object, next_month=False
        )
        assert carry_over_hours == "02:00:00"

    @pytest.mark.django_db
    def test_method_for_carry_over_hours_next_month(
        self, prepared_ReportViewSet_view, report_object
    ):
        """
        Test if method calculates the hours to carry over to next month
        correctly.
        :param prepared_ReportViewSet_view:
        :param report_object:
        :return:
        """
        carry_over_hours = prepared_ReportViewSet_view.calculate_carry_over_hours(
            report_object, next_month=True
        )
        assert carry_over_hours == "-20:00:00"

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
            template_name="api/stundenzettel.html",
            content_dict=export_content,
            pdf_options={
                "page-size": "Letter",
                "margin-top": "30px",
                "margin-right": "5px",
                "margin-bottom": "5px",
                "margin-left": "15px",
                "encoding": "UTF-8",
                "no-outline": None,
            },
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
        with pytest.raises(serializers.ValidationError) as e_info:
            prepared_ReportViewSet_view.check_for_overlapping_shifts(overlapping_shifts)
