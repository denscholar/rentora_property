from decouple import config
from datetime import timedelta
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = [
    "sheltame.com.ng",
    "www.sheltame.com.ng",
]


CSRF_TRUSTED_ORIGINS = [
    "https://sheltame.com.ng",
    "https://www.sheltame.com.ng",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


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
    "property_verification",
    "property_verification_admin",
    # third party packages
    "rest_framework",
    "drf_spectacular",
]

AUTH_USER_MODEL = "accounts.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASSWORD"),
#         "HOST": config("DB_HOST", default="db"),  # "db" = docker-compose service name
#         "PORT": config("DB_PORT", default="5432"),
#     }
# }


DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL"),
    ),
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


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST_FRAMEWORK = {
#     "AUTHENTICATION_WHITELIST": [
#         "rest_framework.authentication.SessionAuthentication",
#     ],
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework.authentication.SessionAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
#     "EXCEPTION_HANDLER": ("core.exceptions.custom_exception_handler"),
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


REST_FRAMEWORK = {
    "AUTHENTICATION_WHITELIST": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": ("drf_spectacular.openapi.AutoSchema"),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": ("core.exceptions.custom_exception_handler"),
}

SPECTACULAR_SETTINGS = {
    # ==========================================
    # PROJECT INFORMATION
    # ==========================================
    "TITLE": "SheltaMe API",
    "DESCRIPTION": """
        ## SheltaMe Property Marketplace API
        SheltaMe is a trust-first property marketplace designed to simplify
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
        "name": "SheltaMe Engineering",
        "email": "engineering@SheltaMe.com",
    },
    "LICENSE": {
        "name": "Copyright ©SheltaMe",
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
    "TAGS": [],
}


CLOUDINARY_CLOUD_NAME = config(
    "CLOUDINARY_CLOUD_NAME",
    default="",
)

CLOUDINARY_API_KEY = config(
    "CLOUDINARY_API_KEY",
    default="",
)

CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", default="", cast=str)

CLOUDINARY_SECURE = config(
    "CLOUDINARY_SECURE",
    default=True,
    cast=bool,
)


RESEND_API_KEY = config("RESEND_API_KEY", default="", cast=str)
RESEND_FROM_EMAIL = config("RESEND_FROM_EMAIL", default="", cast=str)
PROPERTY_VERIFICATION_URL = config("PROPERTY_VERIFICATION_URL", default="", cast=str)


PROPERTY_VERIFICATION_DOCUMENT_MAX_SIZE = 2 * 1024 * 1024  # 2 MB

PROPERTY_VERIFICATION_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
}
