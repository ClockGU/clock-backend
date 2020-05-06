from django.urls import include, path
from rest_framework.routers import DefaultRouter

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

urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path(
        "list-shifts/<int:month>/<int:year>/",
        list_month_year_shifts,
        name="list-shifts",
    ),
    path("gdpr/", GDPRExportView.as_view({"get": "retrieve"})),
    path("", include(router.urls)),
]
