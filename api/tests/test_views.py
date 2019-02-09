# View tests come here

import pytest
import requests
from django.urls import reverse

import json
import jwt
from django.conf import settings
from rest_framework import status
from pytz import datetime
from api.models import Contract, User
from rest_framework.test import RequestsClient


class TestContractApiEndpoint:
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
        Test the create endpoint returns a 401 if no JWT is present
        :param client:
        :param valid_contract_json:
        :return:
        """
        response = client.post(
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
        :param create_n_user_objects:
        :param create_n_contract_objects:
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
        self, client, invalid_uuid_contract_json, user_object, user_object_jwt
    ):
        """
        Test that 'user', 'created_by' and 'modified_by' (incorrectly set invalid_uuid_contract_json)
        are set to the user_id from the JWT of the request.
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
