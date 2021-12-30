from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError


class CustomerManager(BaseUserManager):
    def create_user(self, **data):
        # Redundant try except statement would remove later if verified
        try:
            if not data["email"]:
                raise ValueError(_("The Email Must Be Set"))
        except KeyError as e:
            raise ValueError("the email must be provided")

        data.setdefault("is_active", True)
        email = data.pop("email")
        email = self.normalize_email(email)

        if "@" not in email:
            raise ValidationError(
                {"message": "invalid email"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        user = self.model(email=email, **data)
        user.set_password(data["password"])
        user.save()
        return user

    def create_superuser(self, **data):
        data.setdefault("is_staff", True)
        data.setdefault("is_superuser", True)
        data.setdefault("status", "ACTIVE")

        if data.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if data.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(**data)
