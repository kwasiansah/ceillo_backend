from django.core.cache import cache
from rest_framework.permissions import BasePermission

from customer.models import Merchant


class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return Merchant.objects.filter(customer=request.user).exists()


class IsLoggedOut(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        key = f'{email[:email.index("@")]}_token'
        token = request.auth.__str__()
        return cache.get(key) != token
