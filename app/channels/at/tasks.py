from app.core.tasks import BaseTaskHandler


class AfricasTalkingSendMessageTaskHandler(BaseTaskHandler):
    """
    Africa's Talking send sms message task handler
    """
    name = 'africas-talking.sms.send_message'
    state_transition = True
    support_recon = True
    operation_tag = 'send_africastalking_message'

    def execute(self, params):
        return dict(status=200, data={})
