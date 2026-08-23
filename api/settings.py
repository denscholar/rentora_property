from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import os

SECRET_KEY = "django-insecure-14g51=ckjq^%ijibsfmi0qvw%v1ga6h1=ba+7digz_$@rn8c6b"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "locations",
    "properties",
    "property_moderation",
    "frontend",
    # third party packages
    "rest_framework",
    "drf_spectacular",
]

AUTH_USER_MODEL = "accounts.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "rentoraPropertyDB",
        "USER": "postgres",
        "PASSWORD": "sunshine",
        "HOST": "localhost",
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "AUTHENTICATION_WHITELIST": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": ("core.exceptions.custom_exception_handler"),
}


SPECTACULAR_SETTINGS = {
    # ==========================================
    # PROJECT INFORMATION
    # ==========================================
    "TITLE": "Rentora API",
    "DESCRIPTION": """
        ## Rentora Property Marketplace API
        Rentora is a trust-first property marketplace designed to simplify
        property discovery, viewing bookings, payments, escrow,
        wallets, KYC and property management.
        ### Features
        - Authentication
        - Property Listing
        - Property Discovery
        - Viewing Booking
        - Escrow Payments
        - Wallet
        - Withdrawals
        - Reviews
        - Notifications
        - KYC
        """,
    "VERSION": "1.0.0",
    "CONTACT": {
        "name": "Rentora Engineering",
        "email": "engineering@rentora.com",
    },
    "LICENSE": {
        "name": "Copyright ©Rentora",
    },
    # ==========================================
    # SWAGGER SETTINGS
    # ==========================================
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "persistAuthorization": True,
        "filter": True,
        "displayRequestDuration": True,
        "docExpansion": "list",
    },
    # ==========================================
    # SORTING
    # ==========================================
    "SORT_OPERATIONS": False,
    "SORT_OPERATION_PARAMETERS": False,
    # ==========================================
    # TAGS
    # ==========================================
    "TAGS": [
        # {
        #     "name": "Authentication",
        #     "description": "Authentication and Account APIs",
        # },
        # {
        #     "name": "Users",
        #     "description": "User Profile APIs",
        # },
        # {
        #     "name": "Properties",
        #     "description": "Property APIs",
        # },
        # {
        #     "name": "Bookings",
        #     "description": "Viewing Booking APIs",
        # },
        # {
        #     "name": "Payments",
        #     "description": "Payment APIs",
        # },
        # {
        #     "name": "Wallet",
        #     "description": "Wallet APIs",
        # },
        # {
        #     "name": "KYC",
        #     "description": "Identity Verification APIs",
        # },
        # {
        #     "name": "Admin",
        #     "description": "Administrative APIs",
        # },
    ],
}



CLOUDINARY_CLOUD_NAME = config(
    "CLOUDINARY_CLOUD_NAME",
)

CLOUDINARY_API_KEY = config(
    "CLOUDINARY_API_KEY",
)

CLOUDINARY_API_SECRET = config(
    "CLOUDINARY_API_SECRET",
)

CLOUDINARY_SECURE = config(
    "CLOUDINARY_SECURE",
    default=True,
    cast=bool,
)
