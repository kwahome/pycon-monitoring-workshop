from app.core.tasks import BaseTaskHandler


class FirebasePushNotificationTaskHandler(BaseTaskHandler):
    """
    Firebase send push notification task handler
    """
    name = 'firebase.push.send_message'
    state_transition = True
    support_recon = True
    event_name = 'send_push_notification'

    def execute(self, params):
        self.logger.info(event='{}_start'.format(self.event_name))
        return dict()
