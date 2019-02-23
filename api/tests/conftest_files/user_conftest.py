import pytest

from django.urls import reverse

from api.models import User


@pytest.fixture
def create_n_user_objects():
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
    This Fixture creates a user object which resembles the standart user.
    The standart user symbolize the user sending requests to the api.
    :param create_n_user_objects:
    :return: User
    """
    return create_n_user_objects((1,))[0]


@pytest.fixture
def diff_user_object(create_n_user_objects):
    return create_n_user_objects((1, 2))[0]


@pytest.fixture
def user_object_password():
    return "Test_password"


@pytest.fixture
def user_object_jwt(user_object, client, user_object_password):
    user_response = client.post(
        path=reverse("jwt-create"),
        data={"email": user_object.email, "password": user_object_password},
    )
    return user_response.data["access"]
