from rest_framework import status, views
from rest_framework.response import Response
from app.auth.authentication import APIKeyAuth
from app.auth.permissions import APIPermission
from app.api.serializers import SendMessageRequestSerializer

DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT = \
    'delete', 'get', 'head', 'options', 'patch', 'post', 'put'


class BaseAPIView(views.APIView):
    """
    Base API View class
    """
    authentication_classes = (APIKeyAuth, )
    permission_classes = (APIPermission,)
    allowed_methods = (GET, HEAD, OPTIONS, PATCH, POST, PUT)

    def __init__(self):
        self.req_data = None

    def handler(self, request, *args, **kwargs):
        allowed, response = self.is_allowed(request=request)
        valid, self.req_data = self.validate(request.data)
        if allowed and not valid:
            response = self.bad_request()
        if allowed and valid:
            response = self.handle(request, *args, **kwargs)
        return response

    def post(self, request):
        return self.handler(request, self.post.__name__)

    def get(self, request, *args, **kwargs):
        return self.handler(request, *args, **kwargs)

    def validate(self, data):
        valid = True
        if hasattr(self, 'serializer'):
            serialized = self.serializer(data=data)
            valid = serialized.is_valid()
            if not valid:
                data = serialized.errors
            else:
                data.update(serialized.validated_data)
        return valid, data

    def is_allowed(self, request):
        res = True, None
        if request.method.lower() not in self.allowed_methods:
            res = False, Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                data={
                    'detail': 'Method "{}" not allowed.'.format(
                        request.method)
                },
                content_type="application/json"
            )
        return res

    def bad_request(self):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=self.req_data,
            content_type="application/json"
        )

    def handle(self, request, *args, **kwargs):
        raise NotImplementedError(
            "`handle` method has not been implemented"
        )


class HealthCheckView(BaseAPIView):
    """
    View that monitoring services can use to check on the 'aliveness' of a
    running messaging service.
    """
    allowed_methods = (GET,)

    def handle(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK, content_type="application/json"
        )


class SendMessageView(BaseAPIView):
    """
    View that monitoring services can use to check on the 'aliveness' of a
    running messaging service.
    """
    allowed_methods = (POST,)
    serializer = SendMessageRequestSerializer

    def handle(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_202_ACCEPTED, content_type="application/json"
        )
