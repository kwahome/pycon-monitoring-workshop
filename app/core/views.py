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
    operation_tag = 'base_api_view'

    def __init__(self):
        super(BaseAPIView).__init__()
        self.req_data = None
        self.logger = get_logger(__name__)

    def call_handler(self, request, *args, **kwargs):
        self.logger.info(
            '{0}_request'.format(self.operation),
            view_class=self.__class__.__name__,
            request_method=request.method,
            request_data=request.data
        )
        allowed, response = self.is_allowed(request=request)
        valid, self.req_data = self.validate(request.data)
        if allowed and not valid:
            response = self.respond(
                code=status.HTTP_400_BAD_REQUEST,
                data=self.req_data
            )
        if allowed and valid:
            response = self.handle_request(request, *args, **kwargs)
        self.logger.info(
            '{0}_response'.format(self.operation),
            view_class=self.__class__.__name__,
            status_code=response.status_code,
            response_data=response.data
        )
        return response

    def post(self, request):
        return self.call_handler(request)

    def get(self, request, *args, **kwargs):
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

    @staticmethod
    def respond(code=status.HTTP_200_OK, data=None,
                content_type="application/json"):
        return Response(
            status=code,
            data=data,
            content_type=content_type
        )

    @property
    def operation(self):
        return self.operation_tag

    def handle_request(self, request, *args, **kwargs):
        raise NotImplementedError(
            "`handle` method has not been implemented"
        )
