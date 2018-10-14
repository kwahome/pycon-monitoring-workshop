from app.core.tasks import BaseTaskHandler


class AfricasTalkingSendMessageTaskHandler(BaseTaskHandler):
    """
    Africa's Talking send sms message task handler
    """
    name = 'at.sms.send_message'
    state_transition = True
    support_recon = True
    event_name = 'send_at_message'

    def execute(self, params):
        return dict()
