from django.conf import settings
from rest_framework import permissions


class BaseAPIPermission(permissions.BasePermission):
    """
    Custom permission to only allow requests bearing appropriate api key.
    """
    api_keys = ('',)

    def has_permission(self, request, view):
        """
        returns True if permission is granted, False otherwise.
        """
        permitted = False
        if request.user and request.user.is_authenticated:
            permitted = True
        elif request.auth and request.auth in self.api_keys:
            permitted = True
        return permitted


class APIPermission(BaseAPIPermission):
    api_keys = (settings.API_KEY,)
