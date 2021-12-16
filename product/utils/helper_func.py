import uuid
import hashlib
from django.utils import timezone


def get_url_slug(name):
    unique_id = uuid.uuid4().__str__()[-12::1]
    name = name + " " + unique_id
    slug = name.replace(" ", "-")
    return slug


def get_unique_id():
    hasher = hashlib.md5()
    hasher.update(bytes(str(timezone.now()), encoding='utf8'))
    id = hasher.hexdigest()[:12]
    return id
