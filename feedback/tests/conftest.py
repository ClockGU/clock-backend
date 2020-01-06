import pytest
from feedback.serializers import FeedBackSerializer


@pytest.fixture
def feedback_serializer_field_dict():
    return FeedBackSerializer().get_fields()
