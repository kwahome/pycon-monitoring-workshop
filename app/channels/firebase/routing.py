from app.core.models import MessageChannels
from app.core.routing import PushNotificationAbstractRoutingHandler


class FirebaseRoutingHandler(PushNotificationAbstractRoutingHandler):
    """
    Routing a PUSH notification via firebase
    """
    channel = MessageChannels.FIREBASE.value

    def route_task(self):
        pass
