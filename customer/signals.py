from django.db.models.signals import pre_save
from django.utils import timezone

from .models import Customer


def Passwordhasher(sender, instance, **kwargs):
    instance.last_login = timezone.now()


pre_save.connect(Passwordhasher, sender=Customer)
