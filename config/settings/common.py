"""
Django settings for djangodocker project.

Generated by 'django-admin startproject' using Django dev.5.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from datetime import timedelta

import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("api")

env = environ.Env()


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.APIConfig",
    "project_celery",
    "taggit",
    "rest_framework",
    "drf_yasg",
    "djoser",
    "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "api.oauth.providers.goetheuni",
    "allauth.socialaccount.providers.github",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    "default": env.db(
        "DATABASE_URL", default="postgres://postgres@localhost:5432/postgres"
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# EMAIL
SYSTEM_EMAILS = {
    "RECEIVER": env.str("SYSTEM_EMAIL_RECEIVER", "hello@example.com"),
    "SENDER": env.str("SYSTEM_EMAIL_SENDER", "noreply@example.com"),
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "api.User"

# Simple_JWT
SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.str("DJANGO_SECRET_KEY"),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("api.permissions.AccessOwnDataPermission",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "dj_rest_auth.utils.JWTCookieAuthentication",
    ),
}


# Djoser
DJOSER = {
    "TOKEN_MODEL": None,
    "SERIALIZERS": {
        "user_delete": "api.serializers.DjoserUserSerializer",
        "current_user": "api.serializers.UserSerializer",
    },
}

# django-allauth: Query for the users email,
# but do not prompt for verification
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"

# Return JWT and cookie after logging in
REST_USE_JWT = True
JWT_AUTH_COOKIE = "clock"

# Explicitly allow the frontend URL(s) that will be allowd to access the backend
# Define them as a comma-separated list, i.e.
# CORS_ORIGIN_WHITELIST=https://example.com,https://subdomain.example.com
# A single domain without a trailing comma also works:
# CORS_ORIGIN_WHITELIST=https://example.com
CORS_ORIGIN_WHITELIST = env.tuple("CORS_ORIGIN_WHITELIST", default=())

# The client must provide a `redirect_uri` query parameter when requesting the
# authorization code URL. We retrieve it from the environment.
GOETHE_OAUTH2_REDIRECT_URI = env.str("GOETHE_OAUTH2_REDIRECT_URI", default="")

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "de-DE"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = env.int("SITE_ID", default=1)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

# STATICFILES
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = "/static/"

STATICFILES_DIRS = (str(APPS_DIR.path("static")),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# CELERY STUFF
BROKER_URL = env("RABBITMQ_URL")
CELERY_RESULT_BACKEND = env("RABBITMQ_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ALWAYS_EAGER = True

# Locale

LANGUAGES = [("de", _("German")), ("en", _("English"))]

LOCALE_PATHS = [str(ROOT_DIR("locale"))]
