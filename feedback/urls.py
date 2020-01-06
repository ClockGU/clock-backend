from django.urls import path
from feedback.views import FeedBackView

urlpatterns = [path("feedback", FeedBackView.as_view(), name="feedback")]
