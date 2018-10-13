from django.conf import settings
from rest_framework import authentication, exceptions


class BaseCustomAPIkeyAuth(authentication.BaseAuthentication):
    """
    This creates a custom authentication class that grants access to clients
    that have the right Authorization header value set.
    """
    api_keys = ('',)

    def authenticate(self, request):
        """
        Authenticate the request and returns a tuple of (None, auth) for
        successful api_key authentication, otherwise return None.
        """
        try:
            incoming_api_key = request.META['HTTP_AUTHORIZATION']
        except (AttributeError, KeyError):
            return None
        else:
            if incoming_api_key not in self.api_keys:
                raise exceptions.AuthenticationFailed()
            else:
                return None, incoming_api_key

    def authenticate_header(self, request):
        """
        Returns value for the WWW-Authenticate header in 401 response.
        Otherwise a 403 forbidden response would be generated
        """
        return 'api-key'


class APIKeyAuth(BaseCustomAPIkeyAuth):
    api_keys = (settings.API_KEY, )
