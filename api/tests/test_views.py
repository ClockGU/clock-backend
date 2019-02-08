# View tests come here

import pytest
import requests
from django.urls import reverse

import json
from rest_framework import status

from api.models import Contract


class TestContractApiEndpoint:
    def test_list_not_allowed(self, client):
        response = client.get("http://localhost:8000/api/contracts/")
        assert response.status_code == 501

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

        response = client.post(
            path="/api/contracts/",
            data=invalid_uuid_contract_json,
            header="Authorization: Bearer {}".format(user_object_jwt),
        )

        content = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        new_contract = Contract.objects.get(id=content["id"])

        assert new_contract.user.id == user_object.id
        assert new_contract.created_by.id == user_object.id
        assert new_contract.created_by.id == user_object.id
