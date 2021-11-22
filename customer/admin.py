from django.contrib import admin
from .models import AuthToken, Customer, Merchant
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
# this is only for testing

""" the problem i am having now is that you cannot change customer password on the admin site """


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('photo', 'email', 'phone_number', 'first_name', 'last_name',
                  'password', 'agreed_to_terms', 'is_staff', 'is_superuser', 'status',)

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

    class Meta:
        model = Customer
        fields = ('photo', 'email', 'phone_number', 'first_name', 'last_name',
                  'password', 'agreed_to_terms', 'is_staff', 'is_superuser', 'status',)


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'customer_id',  'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
         'phone_number', 'agreed_to_terms')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('status', 'is_superuser',
         'is_staff', 'user_permissions', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'last_name',  'is_superuser', 'is_staff', 'status', 'password1', 'password2', 'photo', 'agreed_to_terms'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Customer, UserAdmin)

# @admin.register(Customer)
# class AdminCustomer(admin.ModelAdmin):
#     # this is to prevent deletion of customers in the admin panel
#     # this would later be change to a staff account
#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser


@admin.register(Merchant)
class AdminMerchant(admin.ModelAdmin):
    pass


@admin.register(AuthToken)
class AdminAuthToken(admin.ModelAdmin):
    pass
