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
    operation_tag = 'health_check'

    def get_handler(self, request, *args, **kwargs):
        return self.respond()


class SendMessageView(BaseAPIView):
    """
    Send message API view
    """
    allowed_methods = (POST,)
    validator = SendMessageRequestSerializer
    operation_tag = 'send_message'

    def post_handler(self, request, *args, **kwargs):
        try:
            self._init_variables()
            self._init_message_request()
            duplicate, response = self.duplicate_check()
            if not duplicate:
                response = self.route_task()
        except Exception as e:
            self.logger.exception(
                '{0}_exception'.format(self.operation),
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

    def _init_variables(self):
        self.message_id = self.req_data['messageId']
        self.channel = self.req_data["channel"]
        self.message_type = self.req_data["messageType"]
        self.sender_id = self.req_data["senderId"]
        self.recipient_id = self.req_data["recipientId"]
        self.message = self.req_data["message"]
        self.priority = self.req_data["priority"]

    def _init_message_request(self):
        self.message_obj = MessageRequest(
            message_id=self.message_id,
            data=dict(
                sender_id=self.sender_id,
                recipient_id=self.recipient_id,
                message_type=self.message_type,
                channel=self.channel,
                message=self.message,
                priority=self.priority
            )
        )

    def duplicate_check(self):
        result = False, None
        if get_object_or_None(MessageRequest, message_id=self.message_id):
            result = True, self.respond(
                code=status.HTTP_409_CONFLICT,
                data=dict(
                    detail="A message with messageId=`{0}` has already been "
                           "received".format(self.message_id)
                )
            )
        return result

    def route_task(self):
        tag = "routing"
        routing_handler = ROUTING_REGISTRY.get(
            self.message_type, {}
        ).get(self.channel)

        if routing_handler is None:
            error_message = dict(
                details="channel `{0}` and message type `{1}` not "
                        "supported".format(self.channel, self.message_type)
            )
            self.logger.info(
                event='{0}_error'.format(tag),
                message_obj=error_message,
                handler=self.__class__.__name__,
            )
            response = self.respond(
                code=status.HTTP_400_BAD_REQUEST,
                data=error_message
            )
        else:
            self.message_obj.save()
            self.logger.info(
                event='{0}_start'.format(tag),
                message_id=self.message_id,
                handler=self.__class__.__name__,
            )
            routing_handler(self.message_obj).route_task()
            response = self.respond(code=status.HTTP_202_ACCEPTED)
        return response
