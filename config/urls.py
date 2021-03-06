"""djangodocker URL Configuration

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
]"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r"", include("api.urls"), name="api"),
    url(r"", include("api-docs.api_docs"), name="api_docs"),
    url(r"", include("feedback.urls"), name="feedback-app"),
    url(r"", include("message.urls"), name="message-app"),
    url(r"^admin/", admin.site.urls),
    url(r"^auth/", include("djoser.urls"), name="djoser-auth"),
    url(r"^auth/", include("djoser.urls.jwt")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^rosetta/", include("rosetta.urls"))]
