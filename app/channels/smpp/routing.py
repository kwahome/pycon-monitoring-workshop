from app.core.models import MessageChannels
from app.core.routing import SMSAbstractRoutingHandler
from .tasks import SMPPSendMessageTaskHandler


class SMPPRoutingHandler(SMSAbstractRoutingHandler):
    """
    Routing an SMS message via SMPP
    """
    channel = MessageChannels.SMPP.value
    smpp_queue = "smpp.send_message"

    def route_task(self):
        chain = SMPPSendMessageTaskHandler().s(
            self.message_obj.messageId
        )
        chain()
