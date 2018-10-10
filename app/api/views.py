from rest_framework import status, views
from rest_framework.response import Response
from app.auth.authentication import APIKeyAuth
from app.auth.permissions import APIPermission
from app.api.serializers import (
    SendMessageRequestSerializer
)
from app.core.models import MessageModel
from utils.logging import get_logger

DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT = \
    'delete', 'get', 'head', 'options', 'patch', 'post', 'put'


class BaseAPIView(views.APIView):
    """
    Base API View class
    """
    authentication_classes = (APIKeyAuth, )
    permission_classes = (APIPermission,)
    allowed_methods = (GET, DELETE, HEAD, OPTIONS, PATCH, POST, PUT)
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
            response = self.handler(request, *args, **kwargs)
        return response

    def post(self, request):
        self.logger.info(
            event='received',
            handler=self.__class__.__name__,
            request=request.data
        )
        return self.call_handler(request)

    def get(self, request, *args, **kwargs):
        self.logger.info(
            event='received',
            handler=self.__class__.__name__,
            request=request.data
        )
        return self.call_handler(request, *args, **kwargs)

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
            res = False, self.respond(
                code=status.HTTP_405_METHOD_NOT_ALLOWED,
                data=dict(
                    detail='Method "{}" not allowed.'.format(request.method)
                )
            )
        return res

    def respond(self, code=status.HTTP_200_OK, data=None):
        self.logger.info(
            'response',
            status_code=code,
            handler=self.__class__.__name__,
            response_data=data
        )
        return Response(status=code, data=data, content_type="application/json")

    def handler(self, request, *args, **kwargs):
        raise NotImplementedError(
            "`handle` method has not been implemented"
        )


class HealthCheckView(BaseAPIView):
    """
    View that monitoring services can use to check on the 'aliveness' of a
    running messaging service.
    """
    allowed_methods = (GET,)

    def handler(self, request, *args, **kwargs):
        return self.respond()


class SendMessageView(BaseAPIView):
    """
    View that monitoring services can use to check on the 'aliveness' of a
    running messaging service.
    """
    allowed_methods = (POST,)
    serializer = SendMessageRequestSerializer

    def handler(self, request, *args, **kwargs):
        try:
            for message in self.req_data.get("body", list()):
                self._init_message_object(message).save()
                self._dispatcher()

            response = self.respond(
                code=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            self.logger.exception(
                'exception',
                exception=str(e.__class__.__name__),
                message=str(e),
                handler=self.__class__.__name__,
            )
            response = self.respond(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=dict(
                    detail='An internal server error has occured.'
                )
            )
        return response

    def _init_message_object(self, message):
        return MessageModel(
            messageId=message.get("messageId"),
            senderId=message.get("senderId"),
            recipientId=message.get("recipientId"),
            messageType=message.get("messageType"),
            channel=message.get("channel"),
            message=message.get("message"),
            priority=message.get("priority"),
        )

    def _dispatcher(self):
        pass
