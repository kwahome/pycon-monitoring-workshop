from app.core.tasks import BaseTaskHandler


class SMPPSendMessageTaskHandler(BaseTaskHandler):
    """
    SMPP send message task handler
    """
    event_name = 'send_smpp_message'

    def execute(self, params):
        pass
