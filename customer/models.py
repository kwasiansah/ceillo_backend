from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from enum import Enum
from django.contrib.auth.models import User, PermissionsMixin
import uuid
from django.urls import reverse
from django.core.mail.message import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import CustomerManager
from django.db.models.signals import pre_save
from rest_framework.authtoken.models import Token
# Create your models here.

# class Customer(models.Model): # TODO: create the uuid field
# class ACTIVE_CHOICES(Enum):
#     active = ('AC', 'status',)
#     remove = ('RM', 'Removed',)

#     @classmethod
#     def get_value(cls, member):
#         return cls[member].value[0]

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, unique=True, related_name='customer')

#     status = models.CharField(max_length=2, choices=[x.value for x in ACTIVE_CHOICES] , default='AC')
#     photo = models.ImageField(upload_to='profile/' , null=True, blank=True)
#     address = models.CharField(max_length=250, blank=True)
#     created = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.user.username

class Customer(AbstractBaseUser, PermissionsMixin):
    # TODO: over write the is_active field to get extra control over who logs in
    class ACTIVE_CHOICES(Enum):
        active = ('AC', 'status',)
        remove = ('RM', 'Removed',)

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
    customer_id = models.UUIDField(
        default=uuid.uuid4, editable=False, blank=False, null=False, db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    # thinking about making the defalt RM
    status = models.CharField(max_length=2, choices=[
                              x.value for x in ACTIVE_CHOICES], default='AC')
    # first name required
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(
        _('first name'), max_length=150, blank=True, default="")
    # last name required
    last_name = models.CharField(
        _('last name'), max_length=150, blank=False, null=False)
    # email required
    email = models.EmailField(
        _('email address'), blank=False, null=False, unique=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # TODO: create a validator for the phone_number
    '''
    TODO:
    i did not set unique to true because a user can decide to create multiple accounts with the same number
    '''
    phone_number = models.CharField(max_length=10)
    date_of_birth = models.CharField(max_length=11, blank=False)

    photo = models.ImageField(upload_to='profile/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # the terms field is for terms and conditions
    agreed_to_terms = models.BooleanField(default=False)

    address = models.CharField(max_length=250, blank=True, null=False)
    objects = CustomerManager()

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def email_user(self, subject, message, from_email=None, **kwargs):
        # TODO: i would have to set this up later
        pass

    def __str__(self):
        return self.email

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(user.password)
    #     if commit:
    #         user.save()
    #     return user


class Merchant(models.Model):
    # decide wheter to preserve mechant details even after delete
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE,
                                    null=False, blank=False, unique=True, related_name='merchant')
    name = models.CharField(
        max_length=250, help_text='The merchant name you would want to use')
    id_char = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


""" 
this can be used for hashing passwords befor being saved
def Passwordhasher(sender, instance, **kwargs):
    user = instance
    user.set_password(user.password)
    
pre_save.connect(Passwordhasher, sender=Customer)

"""


class AuthToken(Token):
    # i would add the editable attribute later
    key = models.CharField(_('Key'), max_length=40,
                           db_index=True, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("customer"))

    expire = models.DateTimeField()
    type = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.key
