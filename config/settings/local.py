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
import logging

from .common import *

# Try and read a local .env file
# Required to define CORS_ORIGIN_WHITELIST on local machine
env.read_env(env.str("ENV_PATH", ".env"))

INSTALLED_APPS += ["django_extensions", "rosetta"]

# DEBUG
DEBUG = env.bool("DJANGO_DEBUG", default=True)

# SECRET KEY
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="h18i_1j3^d$e6iq8xur&yvbkpk08il9x^&9cf2l2%-0yqx7ss)"
)

# MAIL
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
SYSTEM_EMAIL = env.str("SYSTEM_EMAIL", "no-reply@example.com")

MIDDLEWARE = ["request_logging.middleware.LoggingMiddleware"] + MIDDLEWARE

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "db_app",
        "USER": "db_user" if not env("TRAVIS_CI", default=False) else "postgres",
        "PASSWORD": "db_pass",
        "HOST": "db" if env("PYTHONBUFFERED", default=False) else "localhost",
        "PORT": 5432,
    }
}

# CACHING
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

REQUEST_LOGGING_ENABLE_COLORIZE = True
REQUEST_LOGGING_SENSITIVE_HEADERS = []
REQUEST_LOGGING_HTTP_4XX_LOG_LEVEL = logging.DEBUG
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

ALLOWED_HOSTS = ["*"]
