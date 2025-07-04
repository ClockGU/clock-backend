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
# flake8: noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *

# DEBUG
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# SECRET CONFIGURATION
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY CONFIGURATION
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# PRODUCTION MIDDLEWARE
WHITENOISE_MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE

# STATICFILES
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ALLOWED HOSTS
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Raven Sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

# APPS
INSTALLED_APPS += ("gunicorn",)

# DATABASE
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

EMAIL_HOST = env("DJANGO_EMAIL_HOST", default=None)
EMAIL_PORT = 25
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Glitchtip Configuration
sentry_sdk.init(
    dsn=env("GLITCHTIP_DSN"),
    integrations=[DjangoIntegration()],
    auto_session_tracking=False,
    traces_sample_rate=0,
)

# ADMIN URL
ADMIN_URL = env("DJANGO_ADMIN_URL")
