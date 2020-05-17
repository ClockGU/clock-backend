from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .oauth.views import GitHubLogin, ProviderAuthView

from api.views import (
    ContractViewSet,
    ReportViewSet,
    ShiftViewSet,
    ClockedInShiftViewSet,
    index,
    GDPRExportView,
)

app_name = "api"
router = DefaultRouter()
router.register(r"contracts", ContractViewSet, basename="contracts")
router.register(r"shifts", ShiftViewSet, basename="shifts")
router.register(r"clockedinshifts", ClockedInShiftViewSet, basename="clockedinshifts")
router.register(r"reports", ReportViewSet, basename="reports")

list_month_year_shifts = ShiftViewSet.as_view({"get": "list_month_year"})
lock_shifts = ContractViewSet.as_view({"post": "lock_shifts"})

urlpatterns = [
    path("auth/o/authorize/", ProviderAuthView.as_view(), name="github_auth"),
    path("auth/o/token/", GitHubLogin.as_view(), name="github_login"),
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path(
        "list-shifts/<int:month>/<int:year>/",
        list_month_year_shifts,
        name="list-shifts",
    ),
    path(
        "contracts/<str:pk>/<int:month>/<int:year>/lock",
        lock_shifts,
        name="contracts-lock-shifts",
    ),
    path("gdpr/", GDPRExportView.as_view({"get": "retrieve"})),
    path("", include(router.urls)),
]
