from app.core.models import MessageChannels
from app.core.routing import DummyNotificationAbstractRoutingHandler
from app.core.tasks import SendMessageCallbackHandler
from .tasks import HTTPBINDummyNotificationTaskHandler


class HTTPBINRoutingHandler(DummyNotificationAbstractRoutingHandler):
    """
    Routing a DUMMY notification via httpbin
    """
    channel = MessageChannels.HTTPBIN.value
    message_queue = 'httpbin.dummy.send_message'

    def route_task(self):
        chain = HTTPBINDummyNotificationTaskHandler().s(
            self.message_obj.message_id
        ).set(queue=self.message_queue) | SendMessageCallbackHandler().s(
            self.message_obj.message_id
        ).set()

        chain()
