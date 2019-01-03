import pytest
from api.models import User


@pytest.fixture
def user_model_class_instace():
    return User()

