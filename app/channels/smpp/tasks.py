from app.core.tasks import BaseTaskHandler


class SMPPSendMessageTaskHandler(BaseTaskHandler):
    """
    SMPP send message task handler
    """
    name = 'smpp.sms.send_message'
    state_transition = False
    support_recon = True
    event_name = 'send_smpp_message'

    def execute(self, params):
        return dict(status=200, data={})
