# View tests come here

import pytest
import requests
from django.urls import reverse

import json
from rest_framework import status

from api.models import Contract


class TestContractApiEndpoint:
    def test_list_forbidden_without_jwt(self, client):
        response = client.get(path="http://localhost:8000/api/contracts/")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_list_objects_of_request_user(
        self, client, user_object, user_object_jwt, db_creation_contracts_list_endpoint
    ):
        """
        We test that the list-endpoint only retrieves the Contracts of the User who issues the request.
        :param client:
        :param user_object:
        :param user_object_jwt:
        :param create_n_user_objects:
        :param create_n_contract_objects:
        :return:
        """

        client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user_object_jwt))
        response = client.get(path="http://localhost:8000/api/contracts/")
        data = json.loads(response.content)
        print(data)
        assert response.status_code == 200
        assert all(
            Contract.objects.get(id=contract["id"]).user.id == user_object.id
            for contract in data
        )

    @pytest.mark.django_db
    def test_create_with_correct_user(
        self, client, invalid_uuid_contract_json, user_object, user_object_jwt
    ):
        """
        The invalid uuid_contract_json includes provided data for 'user', 'created_by' and 'modified_by'.
        which is set to the user ID from the JWT of the request.
        :param invalid_uuid_contract_json:
        :param user_object:
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
