import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from .managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    class STATUS_CHOICES(models.TextChoices):
        ACTIVE = ("ACTIVE", "Active")
        REMOVED = ("REMOVED", "Removed")

    class UNIVERSITY_CHOICES(models.TextChoices):
        KNUST = ("KNUST", "Knust")
        UG = ("UG", "UG")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        blank=False,
        null=False,
        db_index=True,
        unique=True,
    )
    is_staff = models.BooleanField(default=False)
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES.choices,
        default=STATUS_CHOICES.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, default=""
    )
    # last name required
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )
    # email required
    email = models.EmailField(
        _("email address"), blank=False, null=False, unique=True
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # TODO: create a validator for the phone_number
    """
    TODO:
    i did not set unique to true because a user can decide to create multiple accounts with the same number
    """
    phone_number = models.CharField(max_length=10)
    #  = models.CharField(max_length=11, blank=False)

    photo = models.ImageField(upload_to="profile/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # the terms field is for terms and conditions
    agreed_to_terms = models.BooleanField(default=False)

    university = models.CharField(
        max_length=5,
        blank=True,
        null=False,
        choices=UNIVERSITY_CHOICES.choices,
    )
    verified_email = models.BooleanField(default=False)
    objects = CustomerManager()

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.email


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    hostel = models.CharField(max_length=250, null=True, blank=True)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    region = models.CharField(max_length=250, blank=True, null=True)


class Merchant(models.Model):
    # decide wheter to preserve mechant details even after delete
    class CARD_TYPES(models.TextChoices):
        NATIONAL = ("National", "National")
        DRIVER = ("Driver", "Driver")
        STUDENT = ("Student", "Student")
        VOTER = ("Voter", "Voter")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        null=False,
    )

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
        related_name="merchant",
    )
    brand = models.CharField(
        max_length=250, help_text="The merchant name you would want to use"
    )
    # Todo change this null to false
    id_card = models.ImageField(upload_to="merchant/", null=True, blank=False)
    id_card_type = models.CharField(
        default=CARD_TYPES.STUDENT, choices=CARD_TYPES.choices, max_length=8
    )

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand


class AuthToken(Token):
    # i would add the editable attribute later
    key = models.CharField(
        _("Key"), max_length=40, db_index=True, unique=True, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name=_("customer"),
    )

    expire = models.DateTimeField()
    type = models.CharField(max_length=250, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
