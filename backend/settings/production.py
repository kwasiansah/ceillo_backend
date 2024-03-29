import dj_database_url

from . import base
from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")


DEBUG = True


ALLOWED_HOSTS = [
    "*",
]


# INSTALLED_APPS
PRODUCTION_APPS = [
    "whitenoise.runserver_nostatic",
]

base.INSTALLED_APPS += PRODUCTION_APPS


# CACHES
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:p91b5344cb01bbe9a5e8070a07fd08afd035588d052ff90c332b9a11d10a91082@ec2-3-209-0-252.compute-1.amazonaws.com:26900",
#         "OPTION": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ.get("DB_USERNAME"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "postgres",
            "PORT": os.environ.get("POSTGRES_PORT"),
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get("CACHE_REDIS_LOCATION"),
            "OPTION": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }


# STATIC FILES
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# STATICFILES_DIRS  = (os.path.join(BASE_DIR, 'static'),)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_STORAGE = (
    "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
)
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# DEBUG TOOLBAR IPS
INTERNAL_IPS = [
    "127.0.0.1",
    "ceillo-app.herokuapp.com",
]


# CORS HEADERS
CORS_ALLOW_ALL_ORIGINS = True


# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


X_FRAME_OPTIONS = "SAMEORIGIN"

SILENCED_SYSTEM_CHECKS = ["security.W019"]


# CLOUDINARY
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}


# FILE
FILE_UPLOAD_MAX_MEMORY_SIZE = 5621440


# CUSTOM SETTINGS

# this defines the time it takes the token to expire
EMAIL_RESET_TOKEN_TIMEOUT_MIN = 60
