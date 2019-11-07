from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ContractViewSet,
    ReportViewSet,
    ShiftViewSet,
    ClockedInShiftViewSet,
    index,
)

app_name = "api"
router = DefaultRouter()
router.register(r"contracts", ContractViewSet, base_name="contracts")
router.register(r"shifts", ShiftViewSet, base_name="shifts")
router.register(r"clockedinshifts", ClockedInShiftViewSet, base_name="clockedinshifts")
router.register(r"reports", ReportViewSet, base_name="reports")

list_month_year_shifts = ShiftViewSet.as_view({"get": "list_month_year"})

urlpatterns = [
    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path(
        "list-shifts/<int:month>/<int:year>/",
        list_month_year_shifts,
        name="list-shifts",
    ),
    path("", include(router.urls)),
]
