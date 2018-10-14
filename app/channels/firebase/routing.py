from app.core.models import MessageChannels
from app.core.routing import PushNotificationAbstractRoutingHandler
from app.core.tasks import SendMessageCallbackHandler
from .tasks import FirebasePushNotificationTaskHandler


class FirebaseRoutingHandler(PushNotificationAbstractRoutingHandler):
    """
    Routing a PUSH notification via firebase
    """
    channel = MessageChannels.FIREBASE.value
    message_queue = "{0}.{1}.send_message".format(
        channel, PushNotificationAbstractRoutingHandler.message_type
    )

    def route_task(self):
        chain = FirebasePushNotificationTaskHandler().s(
            self.message_obj.message_id
        ).set(queue=self.message_queue) | SendMessageCallbackHandler().s(
            self.message_obj.message_id
        ).set()

        chain()
