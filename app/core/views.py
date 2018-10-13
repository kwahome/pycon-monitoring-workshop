from rest_framework import status, views
from rest_framework.response import Response
from app.auth.authentication import APIKeyAuth
from app.auth.permissions import APIPermission
from utils.logging import get_logger

DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT = \
    'delete', 'get', 'head', 'options', 'patch', 'post', 'put'


class BaseAPIView(views.APIView):
    """
    Base API View class that should be inherited by all API views.

    Inherits from DRF APIView & implements custom logic that would otherwise
    be duplicated on every view class.

    Children classes must implement the `handle_request` method which
    describes/implements the behaviour of how an API request should be fulfilled
    """
    authentication_classes = (APIKeyAuth, )
    permission_classes = (APIPermission,)
    allowed_methods = (GET, DELETE, HEAD, OPTIONS, PATCH, POST, PUT)
    event = 'base_api_view'
    logger = get_logger(__name__)

    def __init__(self):
        super(BaseAPIView).__init__()
        self.req_data = None

    def call_handler(self, request, *args, **kwargs):
        allowed, response = self.is_allowed(request=request)
        valid, self.req_data = self.validate(request.data)
        if allowed and not valid:
            response = self.respond(
                code=status.HTTP_400_BAD_REQUEST,
                data=self.req_data
            )
        if allowed and valid:
            response = self.handle_request(request, *args, **kwargs)
        return response

    def post(self, request):
        self.logger.info(
            '{0}_request'.format(self.event),
            handler=self.__class__.__name__,
            request=request.data
        )
        return self.call_handler(request)

    def get(self, request, *args, **kwargs):
        self.logger.info(
            '{0}_request'.format(self.event),
            handler=self.__class__.__name__,
            request=request.data
        )
        return self.call_handler(request, *args, **kwargs)

    def validate(self, data):
        valid = True
        if hasattr(self, 'validator'):
            serialized = self.validator(data=data)
            valid = serialized.is_valid()
            if not valid:
                data = serialized.errors
            else:
                data.update(serialized.validated_data)
        return valid, data

    def is_allowed(self, request):
        res = True, None
        if request.method.lower() not in self.allowed_methods:
            res = False, self.respond(
                code=status.HTTP_405_METHOD_NOT_ALLOWED,
                data=dict(
                    detail='Method "{}" not allowed.'.format(request.method)
                )
            )
        return res

    def respond(self, code=status.HTTP_200_OK, data=None):
        self.logger.info(
            '{0}_response'.format(self.event),
            status_code=code,
            handler=self.__class__.__name__,
            response_data=data
        )
        return Response(status=code, data=data, content_type="application/json")

    def handle_request(self, request, *args, **kwargs):
        raise NotImplementedError(
            "`handle` method has not been implemented"
        )
