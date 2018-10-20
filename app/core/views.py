import time
from six import with_metaclass
from rest_framework import status, views
from rest_framework.response import Response
from app.auth.authentication import APIKeyAuth
from app.auth.permissions import APIPermission
from utils.logging import get_logger

DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT = \
    'delete', 'get', 'head', 'options', 'patch', 'post', 'put'


class APIViewMetaClass(type):
    """
    Metaclass to validate that an APIView class extending the abstract
    BaseAPIView class has a handler for each of the allowed methods/operations.

    It also dynamically adds the appropriate APIView handler method for each
    REST operation (read as verb) allowed e.g. delete, get, patch, post, put.

    It does not operate on any class object with the attribute `abstract` set
    to True.
    """

    def __init__(cls, name, bases, attr):
        super(APIViewMetaClass, cls).__init__(name, bases, attr)

        def _abstract_method(self, request, *args, **kwargs):
            """
            Abstract method to handle a REST operation (read as verb)
            e.g. delete, get, patch, post, put.

            This method will be dynamically added/injected into the class
            object as it's being validated & loaded.
            """
            return self.handle(request, *args, **kwargs)

        if not attr.get('abstract', False):
            for attr in attr.get('allowed_methods', ()):
                setattr(cls, attr, _abstract_method)
                required_method = '{0}_handler'.format(attr)
                if not hasattr(cls, required_method):
                    raise NotImplementedError(
                        """Required method {0} has not been implemented in 
                        class {1}""".format(required_method, name)
                    )


class BaseAPIView(with_metaclass(APIViewMetaClass, views.APIView)):
    """
    Base API View class that should be inherited by all API views.

    Inherits from DRF APIView & implements custom logic that would otherwise
    be duplicated on every view class.

    Children classes must implement a handler method for each of the allowed
    methods named with the below signature:

        def <REST operation>_handler(self, request, *args, **kwargs):
                # do stuff for this operation

    e.g.
        def get_handler(self, request, *args, **kwargs)
            # do stuff for a get request

    This method describes/implements the behaviour of how an API request should
    be fulfilled and will be called for every request of that method.

    Extending this class only requires you to:
        1. override the `allowed_methods` class attribute which defines a tuple
        indicating what API requests are permitted; e.g.

            allowed_methods = ('get', 'patch', 'post')

        2. implement a handler method for each of the allowed methods with a
        signature as described in paragraphs above.
    """
    abstract = True
    authentication_classes = (APIKeyAuth, )
    permission_classes = (APIPermission,)
    allowed_methods = (GET, DELETE, HEAD, OPTIONS, PATCH, POST, PUT)
    operation_tag = ''

    def __init__(self):
        super(BaseAPIView).__init__()
        self.req_data = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.logger = get_logger(__name__).bind(
            operation="{0}_view".format(self.operation)
        )

    def initial(self, request, *args, **kwargs):
        self.start_time = time.time()
        self.logger.info(
            event='request',
            start_time=self.start_time,
            view_class=self.__class__.__name__,
            request_method=request.method,
            request_data=request.data
        )
        super(BaseAPIView, self).initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time) * 1000
        self.logger.info(
            event='response',
            view_class=self.__class__.__name__,
            status_code=response.status_code,
            response_data=response.data,
            duration_millis=self.duration
        )
        return super(BaseAPIView, self).finalize_response(
            request, response, *args, **kwargs)

    def handle(self, request, *args, **kwargs):
        allowed, response = self.is_allowed(request=request)
        valid, self.req_data = self.validate(request.data)
        if allowed and valid:
            handler = '{0}_handler'.format(request.method.lower())
            try:
                response = getattr(self, handler)(request, *args, **kwargs)
            except Exception as e:
                self.logger.exception(
                    '{0}_exception'.format(self.operation),
                    exception=str(e.__class__.__name__),
                    message=str(e),
                    view_class=self.__class__.__name__
                )
                response = self.internal_server_error()
        else:
            response = self.bad_request()
        return response

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
            res = False, self.http_method_not_allowed(request=request)
        return res

    def bad_request(self, data=None):
        return self.respond(
            code=status.HTTP_400_BAD_REQUEST,
            data=data or self.req_data
        )

    def conflicting_request(self, data=None):
        return self.respond(code=status.HTTP_409_CONFLICT, data=data)

    def internal_server_error(self, data=None):
        return self.respond(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=data or dict(detail='An internal server error has occurred.')
        )

    def request_accepted(self, data=None):
        return self.respond(code=status.HTTP_202_ACCEPTED, data=data)

    @staticmethod
    def respond(code=status.HTTP_200_OK, data=None,
                content_type="application/json"):
        return Response(status=code, data=data, content_type=content_type)

    @property
    def operation(self):
        return self.operation_tag
