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
"""
djangodocker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add, include('apiapi.urls')),
    url(r'^admin/', admin.site.urls),
]
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r"", include("api.urls"), name="api"),
    url(r"", include("api-docs.api_docs"), name="api_docs"),
    url(r"", include("feedback.urls"), name="feedback-app"),
    url(r"", include("message.urls"), name="message-app"),
    url(r"", include("faq.urls"), name="faq-app"),
    url(r"^admin/", admin.site.urls),
    url(r"^auth/", include("djoser.urls"), name="djoser-auth"),
    url(r"^auth/", include("djoser.urls.jwt")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^rosetta/", include("rosetta.urls"))]
