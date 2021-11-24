from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
# TODO: check the use of the ugettext_lazy

class CustomerManager(BaseUserManager):
    
    def create_user(self, **data):
        
        if not data['email']:
            raise ValueError(_('The Email Must Be Set'))
        # TODO: may also consider creating a check for the username field
        email = data.pop('email')
        email = self.normalize_email(email)
        user = self.model(email=email, **data)
        user.set_password(data['password'])
        user.save()
        return user
    
    def create_superuser(self, **data):
        data.setdefault('is_staff', True)
        data.setdefault('is_superuser', True)
        data.setdefault('status', 'AC')
        if data.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if data.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(**data)
