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
    email = "test{}@test.com"
    first_name = "Testfirstname"
    last_name = "Testlastname"
    personal_number = "1234567890"
    password = "Test_password"

    def create_users(start_stop):
        return [
            User.objects.create_user(
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
def diff_user_object(create_n_user_objects):
    """
    This fixture creates a user object which resembles a user which tries to eploit the system by accessing other
    users data.
    :param create_n_user_objects:
    :return:
    """
    return create_n_user_objects((1, 2))[0]


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
