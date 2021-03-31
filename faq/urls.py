from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FaqViewSet

app_name = "faq"

router = DefaultRouter()
router.register(r"faq", FaqViewSet, basename="faqs")

urlpatterns = [path("", include(router.urls))]
