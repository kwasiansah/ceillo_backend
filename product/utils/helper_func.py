import uuid
import hashlib
from django.utils import timezone


def get_unique_id():
    hasher = hashlib.md5()
    hasher.update(bytes(str(timezone.now()), encoding="utf8"))
    id = hasher.hexdigest()[:12]
    return id


def get_url_slug(name):
    # unique_id = uuid.uuid4().__str__()[-12::1]
    unique_id = get_unique_id()
    name = name + " " + unique_id
    slug = name.replace(" ", "-")
    return slug


def get_product_image(obj):
    # url = obj.media.all()[0].raw_image.url if obj.media.first(
    # ) else "/media/default/default.jpg"
    # vid = obj.media.all()[0].video.url if obj.media.first(
    # ) else "/media/default/default.jpg"

    try:
        url = obj.media.all()[0].raw_image.url
    except IndexError:
        url = "/media/default/default.jpg"
    print("this", url)
    try:

        vid = obj.media.all()[0].video.url
    except IndexError:
        vid = "/media/default/defaultvid.mp4"
    print(vid)
    return url, vid
