# View tests come here

import json
from datetime import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

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
            path=reverse("api:contracts-detail", args=[diff_user_contract_object.id])
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
        response = client.get(path=r"/api/contracts/", args=[contract_object.id])
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_list_forbidden_without_jwt(self, client):
        """
        Test the list endpoint returns a 401 if no JWT is present.
        :param client:
        :return:
        """
        response = client.get(path="http://localhost:8000/api/contracts/")
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
            path="http://localhost:8000/api/contracts/", data=valid_contract_json
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
            path="http://localhost:8000/api/contracts/", data=valid_contract_json
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
        response = client.get(path="http://localhost:8000/api/contracts/")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert all(
            Contract.objects.get(id=contract["id"]).user.id == user_object.id
            for contract in data
        )

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
        response = client.post(path="/api/contracts/", data=invalid_uuid_contract_json)

        content = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        new_contract = Contract.objects.get(id=content["id"])

        assert new_contract.user.id == user_object.id
        assert new_contract.created_by.id == user_object.id
        assert new_contract.created_by.id == user_object.id

    @pytest.mark.django_db
    def test_update_uuid_contract(
        self,
        client,
        invalid_uuid_contract_put_endpoint,
        contract_object,
        user_object,
        user_object_jwt,
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

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:contracts-detail", args=[contract_object.id]),
            data=invalid_uuid_contract_put_endpoint,
        )
        content = json.loads(response.content)

        assert response.status_code == 200
        # Check that neither "user", "created_by" nor "modified_by" changed from the originial/issuing user
        user_id = user_object.id
        contract = Contract.objects.get(id=contract_object.id)
        assert contract.user.id == user_id
        assert contract.created_by.id == user_id
        assert contract.modified_by.id == user_id
        #      New Datetime           Old Datetime  --> Result should be positive
        assert contract.modified_at > contract_object.modified_at

    @pytest.mark.django_db
    def test_patch_uuid_contract(
        self,
        client,
        invalid_uuid_contract_patch_endpoint,
        contract_object,
        user_object,
        user_object_jwt,
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
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.patch(
            path=reverse("api:contracts-detail", args=[contract_object.id]),
            data=invalid_uuid_contract_patch_endpoint,
        )
        contract = Contract.objects.get(id=contract_object.id)
        user_id = user_object.id
        assert response.status_code == 200

        assert contract.user.id == user_id
        assert contract.created_by.id == user_id
        assert contract.modified_by.id == user_id
        #      New Datetime           Old Datetime  --> Result should be positive
        assert contract.modified_at > contract_object.modified_at

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
            path=reverse("api:contracts-shifts", args=[contract_object.id])
        )

        content = json.loads(response.content)

        assert len(content) == 2  # We created only 2 shifts for the User
        assert all(shift["contract"] == str(contract_object.id) for shift in content)

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
        response = client.post(path="/api/contracts/", data=valid_contract_json)

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
        response = client.get(path=reverse("api:shifts-list"))

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
        response = client.post(path=reverse("api:shifts-list"), data=valid_shift_json)
        data = json.loads(response.content)

        assert response.status_code == 201
        shift_object = Shift.objects.get(pk=data["id"])
        initial_tags = json.loads(valid_shift_json["tags"])

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
            data=put_new_tags_json,
        )

        data = json.loads(response.content)
        initial_tags = json.loads(put_new_tags_json["tags"])

        assert response.status_code == 200
        shift_object = Shift.objects.get(pk=put_new_tags_json["id"])
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
            data=patch_new_tags_json,
        )

        initial_tags = json.loads(patch_new_tags_json["tags"])

        assert response.status_code == 200
        shift_object = Shift.objects.get(pk=patch_new_tags_json["id"])

        assert shift_object.tags.all().count() == len(initial_tags)
        assert all(
            shift_tag.name in initial_tags for shift_tag in shift_object.tags.all()
        )

    @pytest.mark.django_db
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
        response = client.get(path=reverse("api:list-shifts", args=[1, 2019]))

        data = json.loads(response.content)

        assert response.status_code == 200
        assert len(data) == 2
        assert all(
            datetime.strptime(i["started"], "%Y-%m-%dT%H:%M:%SZ").month == 1
            and datetime.strptime(i["started"], "%Y-%m-%dT%H:%M:%SZ").year == 2019
            for i in data
        )

    @pytest.mark.django_db
    def test_updating_exported_shift_returns_403(
        self, client, user_object_jwt, put_to_exported_shift_json
    ):
        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.put(
            path=reverse("api:shifts-detail", args=[put_to_exported_shift_json["id"]]),
            data=put_to_exported_shift_json,
        )
        assert response.status_code == 403


class TestReportApiEndpoint:
    @freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_get_current_endpoint(
        self, client, user_object_jwt, db_get_current_endpoint
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
        response = client.get(path=reverse("api:reports-get_current"))
        content = json.loads(response.content)

        assert content["month_year"] == "2019-01-01"
