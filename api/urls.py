"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ClockedInShiftViewSet,
    ContractViewSet,
    GDPRExportView,
    ReportViewSet,
    ShiftViewSet,
    index,
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

    # Demonstration url for celery
    path("celery-dummy", index, name="index"),
    path(
        "list-shifts/<int:month>/<int:year>/",
        list_month_year_shifts,
        name="list-shifts",
    ),
    path(
        "contracts/<str:pk>/<int:month>/<int:year>/lock/",
        lock_shifts,
        name="contracts-lock-shifts",
    ),
    path("gdpr/", GDPRExportView.as_view({"get": "retrieve"})),
    path("", include(router.urls)),
]
