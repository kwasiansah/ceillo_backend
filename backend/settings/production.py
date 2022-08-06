import dj_database_url

from . import base
from .base import *

SECRET_KEY = "=%gglh9$vmlbah*d(o!6x+l%l60t%+q$m)w%vxtz2ag=m)q7sj"


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
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:p91b5344cb01bbe9a5e8070a07fd08afd035588d052ff90c332b9a11d10a91082@ec2-3-209-0-252.compute-1.amazonaws.com:26900",
        "OPTION": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "d6d0cq9nmvoin8",
        "USER": "rbrdpyhintglrw",
        "PASSWORD": (
            "2d71ffb2e1c7ffcd820a78e6230e19e0d70128bce2bc90967bcce9fbfcd0acd2"
        ),
        "HOST": "ec2-44-199-40-188.compute-1.amazonaws.com",
        "PORT": "5432",
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
DEFAULT_FROM_EMAIL = "ceillogh@gmail.com"
EMAIL_HOST_USER = "ceillogh@gmail.com"
EMAIL_HOST_PASSWORD = "ceillo@123"


X_FRAME_OPTIONS = "SAMEORIGIN"

SILENCED_SYSTEM_CHECKS = ["security.W019"]


# CLOUDINARY
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "ha8rp7uvj",
    "API_KEY": "124267939288912",
    "API_SECRET": "hYc8kADJiaPpdWAQQO7I2qfIpxk",
}


# FILE
FILE_UPLOAD_MAX_MEMORY_SIZE = 5621440


# CUSTOM SETTINGS

# this defines the time it takes the token to expire
EMAIL_RESET_TOKEN_TIMEOUT_MIN = 60
