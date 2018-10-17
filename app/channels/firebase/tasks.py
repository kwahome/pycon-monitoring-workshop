from app.core.tasks import BaseTaskHandler


class FirebasePushNotificationTaskHandler(BaseTaskHandler):
    """
    Firebase send push notification task handler
    """
    name = 'firebase.push.send_message'
    state_transition = True
    support_recon = True
    operation_tag = 'send_push_notification'

    def execute(self, params):
        return dict(status=200, data={})
