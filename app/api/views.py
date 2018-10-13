from annoying.functions import get_object_or_None
from app.api.serializers import (
    SendMessageRequestSerializer
)
from app.core.models import MessageRequest
from app.core.routing import ROUTING_REGISTRY
from app.core.views import (
    BaseAPIView, GET, POST
)
from rest_framework import status


class HealthCheckView(BaseAPIView):
    """
    View that monitoring services can use to check on the 'aliveness' of a
    running messaging service.
    """
    allowed_methods = (GET,)
    event = 'health_check'

    def handle_request(self, request, *args, **kwargs):
        return self.respond()


class SendMessageView(BaseAPIView):
    """
    Send message API view
    """
    allowed_methods = (POST,)
    validator = SendMessageRequestSerializer
    event = 'send_message'

    def __init__(self):
        super(SendMessageView, self).__init__()
        self.message_obj = None
        self.channel = None
        self.message_type = None

    def handle_request(self, request, *args, **kwargs):
        try:
            duplicate, response = self.duplicate_check()
            if not duplicate:
                self.message_obj = self.message_object()
                response = self.route_task()
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

    def duplicate_check(self):
        result = False, None
        message_id = self.req_data.get('messageId')
        if get_object_or_None(MessageRequest, messageId=message_id):
            message = "A message with messageId=`{0}` has already been " \
                      "received".format(message_id)
            self.logger.info(
                'duplicate_message',
                details=message,
                handler=self.__class__.__name__,
            )
            result = True, self.respond(
                code=status.HTTP_409_CONFLICT,
                data=dict(
                    detail=message
                )
            )
        return result

    def message_object(self):
        self.logger.info(
            'initializing_message_object',
            request=self.req_data,
            handler=self.__class__.__name__,
        )
        self.channel = self.req_data.get("channel")
        self.message_type = self.req_data.get("messageType")
        return MessageRequest(
            messageId=self.req_data.get("messageId"),
            messageType=self.message_type,
            data=dict(
                senderId=self.req_data.get("senderId"),
                recipientId=self.req_data.get("recipientId"),
                messageType=self.message_type,
                channel=self.channel,
                message=self.req_data.get("message"),
                priority=self.req_data.get("priority")
            )
        )

    def route_task(self):
        routing_handler = ROUTING_REGISTRY.get(
            self.message_type, {}
        ).get(self.channel)

        if routing_handler is None:
            error_message = dict(
                details="channel `{0}` and message type `{1}` not "
                        "supported".format(self.channel, self.message_type)
            )
            self.logger.info(
                'routing_message_task_error',
                message_obj=error_message,
                handler=self.__class__.__name__,
            )
            response = self.respond(
                code=status.HTTP_400_BAD_REQUEST,
                data=error_message
            )
        else:
            self.logger.info(
                'routing_message_task',
                message_obj=self.message_obj,
                handler=self.__class__.__name__,
            )
            self.message_obj.save()
            routing_handler(self.message_obj).route_task()
            response = self.respond(code=status.HTTP_202_ACCEPTED)
        return response
