from app.core.models import MessageChannels
from app.core.routing import SMSAbstractRoutingHandler


class AfricasTalkingRoutingHandler(SMSAbstractRoutingHandler):
    """
    Routing an SMS via Africa's Talking
    """
    channel = MessageChannels.AT.value

    def route_task(self):
        pass
