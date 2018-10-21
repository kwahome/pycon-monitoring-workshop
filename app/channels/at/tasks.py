from app.core.tasks import BaseTaskHandler
from app.lib.at.africas_talking import AfricasTalkingClient
from django.conf import settings


class AfricasTalkingSendMessageTaskHandler(BaseTaskHandler):
    """
    Africa's Talking send sms message task handler
    """
    name = 'africas-talking.sms.send_message'
    state_transition = True
    support_recon = True
    operation_tag = 'send_africastalking_message'

    def execute(self, params):
        results = AfricasTalkingClient(
            settings.AFRICAS_TALKING_USERNAME,
            settings.AFRICAS_TALKING_API_KEY
        ).send_message(
            params.recipients, params.message
        )
        self.message_obj.data['status']['results'] = results
        return results
