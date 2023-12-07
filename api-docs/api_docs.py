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
import environ
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# This is the documentation for the API, generated for swagger and Redoc standart
env = environ.Env()
base_url = "https://{}".format(env("DJANGO_ALLOWED_HOSTS", default="localhost:8000"))
contact_mail = env("CONTACT_MAIL", default="")

schema_view = get_schema_view(
    openapi.Info(
        title="Clock API",
        default_version="v1.0",
        description="This is the API for the project Clock",
        contact=openapi.Contact(email=contact_mail),
    ),
    # validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=base_url,
)

app_name = "api_docs"
urlpatterns = [
    re_path(
        r"^swagger(?P<format>.json|.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=None),
        name="schema-redoc",
    ),
]
