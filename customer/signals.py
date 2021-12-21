from django.db.models.signals import pre_save
from .models import Customer
from django.utils import timezone


def Passwordhasher(sender, instance, **kwargs):
    instance.last_login = timezone.now()


pre_save.connect(Passwordhasher, sender=Customer)
