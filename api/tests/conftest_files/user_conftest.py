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
import pytest
from django.urls import reverse

from api.models import User

# This conftest file provides all necessary test data concerning the User Model.
# It will be imported by the conftest.py in the parent directory.


@pytest.fixture
def create_n_user_objects():
    """
    This fixture resembles a user object factory.
    Since the users are distinguished by email the factory generates emails of the format
    test<int>@test.com.
    :return: Function
    """
    username = "testusername{}"
    email = "test{}@test.com"
    first_name = "Testfirstname"
    last_name = "Testlastname"
    personal_number = "1234567890"
    password = "Test_password"

    def create_users(start_stop):
        return [
            User.objects.create(
                username=username.format(i),
                email=email.format(i),
                first_name=first_name,
                last_name=last_name,
                personal_number=personal_number,
                password=password,
            )
            for i in range(*start_stop)
        ]

    return create_users


@pytest.fixture
def user_object(create_n_user_objects):
    """
    This fixture creates a user object which resembles the standart user.
    The standart user symbolize the user sending requests to the api within tests.
    :param create_n_user_objects:
    :return: User
    """
    return create_n_user_objects((1,))[0]


@pytest.fixture
def user_object_json(user_object):
    data = {
        "email": user_object.email,
        "first_name": user_object.first_name,
        "last_name": user_object.last_name,
        "personal_number": user_object.personal_number,
        "password": user_object.password,
    }
    return data


@pytest.fixture
def diff_user_object(create_n_user_objects):
    """
    This fixture creates a user object which resembles a user which tries to eploit the system by accessing other
    users data.
    :param create_n_user_objects:
    :return:
    """
    return create_n_user_objects((1, 2))[0]


@pytest.fixture
def report_update_user(create_n_user_objects):
    return create_n_user_objects((10, 11))[0]


@pytest.fixture
def user_object_password():
    """
    This fixture provides the password of the standart user in clean, unhased form. It will be needed in the following
    fixture to access the users jwt.
    We can not acces the clean, unhased passwort via the user_object fixture since it's retrieved in a hased form form
    the database.
    :return: string
    """
    return "Test_password"


@pytest.fixture
def user_object_jwt(user_object, client, user_object_password):
    """
    This fixture retrieves the standart users valid JWT.

    :param user_object:
    :param client:
    :param user_object_password:
    :return: string
    """
    user_response = client.post(
        path=reverse("jwt-create"),
        data={"email": user_object.email, "password": user_object_password},
    )
    return user_response.data["access"]
