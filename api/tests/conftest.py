import pytest
from api.models import User, Contract


@pytest.fixture
def user_model_class_instace():
    return User()


@pytest.fixture
def contract_model_class_instance():
    return Contract()
