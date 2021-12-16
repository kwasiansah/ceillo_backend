from rest_framework.permissions import BasePermission
from django.core.cache import cache


class IsLoggedOut(BasePermission):

    def has_permission(self, request, view):
        email = request.user.email
        key = f'{email[:email.index("@")]}_token'
        token = request.auth.__str__()
        print(cache.get(key))
        return cache.get(key) != token
