from app.core.models import MessageChannels
from app.core.routing import SMSAbstractRoutingHandler
from app.core.tasks import SendMessageCallbackHandler
from .tasks import SMPPSendMessageTaskHandler


class SMPPRoutingHandler(SMSAbstractRoutingHandler):
    """
    Routing an SMS message via SMPP
    """
    channel = MessageChannels.SMPP.value
    message_queue = "{0}.{1}.send_message".format(
        channel, SMSAbstractRoutingHandler.message_type
    )
    callback_queue = "all.callback.send_message"

    def route_task(self):
        chain = SMPPSendMessageTaskHandler().s(
            self.message_obj.message_id
        ).set(queue=self.message_queue) | SendMessageCallbackHandler().s(
            self.message_obj.message_id
        ).set()

        chain()
