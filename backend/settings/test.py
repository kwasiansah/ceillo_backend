from .base import *

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR.parent, "email")

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
