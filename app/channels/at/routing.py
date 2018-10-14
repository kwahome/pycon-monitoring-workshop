from app.core.models import MessageChannels
from app.core.routing import SMSAbstractRoutingHandler
from app.core.tasks import SendMessageCallbackHandler
from .tasks import AfricasTalkingSendMessageTaskHandler


class AfricasTalkingRoutingHandler(SMSAbstractRoutingHandler):
    """
    Routing an SMS via Africa's Talking
    """
    channel = MessageChannels.AT.value
    message_queue = "{0}.{1}.send_message".format(
        channel, SMSAbstractRoutingHandler.message_type
    )

    def route_task(self):
        chain = AfricasTalkingSendMessageTaskHandler().s(
            self.message_obj.message_id
        ).set(queue=self.message_queue) | SendMessageCallbackHandler().s(
            self.message_obj.message_id
        ).set()

        chain()
