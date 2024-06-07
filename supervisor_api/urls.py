from django.urls import path

from supervisor_api.views import ReportingEndpoint, VerifyEndpoint

urlpatterns = [
    path("verify/", VerifyEndpoint.as_view(), name="verify"),
    path(
        "reports/<int:month>/<int:year>/", ReportingEndpoint.as_view(), name="reports"
    ),
]
