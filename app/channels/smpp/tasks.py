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
        self.logger.info(event='{}_start'.format(self.event_name))
        return dict()
