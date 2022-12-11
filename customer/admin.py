from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import (
    OutstandingTokenAdmin,
)

from .models import AuthToken, Customer, Merchant

# this is only for testing

""" the problem i am having now is that you cannot change customer password on the admin site """


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Customer
        fields = (
            "photo",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
            "agreed_to_terms",
            "is_staff",
            "is_superuser",
            "status",
            "university",
            "verified_email",
        )

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()
    # TODO; Remove Email a user should not be able to change email
    class Meta:
        model = Customer
        fields = (
            "photo",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
            "agreed_to_terms",
            "is_staff",
            "is_active",
            "is_superuser",
            "status",
            "university",
            "verified_email",
        )


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "id", "is_superuser", "is_active")
    list_filter = ("is_superuser",)
    readonly_fields = ("last_login", "thumbnail_image")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "phone_number",
                    "agreed_to_terms",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "photo",
                    "last_login",
                    "university",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "verified_email",
                    "status",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "user_permissions",
                    "groups",
                    "thumbnail_image",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "university",
                    "verified_email",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "status",
                    "password1",
                    "password2",
                    "photo",
                    "agreed_to_terms",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ("user_permissions", "groups")

    @admin.display(description="profile image")
    def thumbnail_image(self, obj):

        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.photo.url,
                width=200,
                height=200,
            )
        )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Customer, UserAdmin)


@admin.register(Merchant)
class AdminMerchant(admin.ModelAdmin):
    list_display = ["brand", "id", "id_card_type"]
    readonly_fields = ("id_card_image",)

    def id_card_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.id_card.url,
                width=200,
                height=200,
            )
        )


@admin.register(AuthToken)
class AdminAuthToken(admin.ModelAdmin):
    list_display = ["user", "type", "created"]


class CeilloOutstandinTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, request, obj=None, **kwargs):

        return request.user.is_superuser


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, CeilloOutstandinTokenAdmin)
