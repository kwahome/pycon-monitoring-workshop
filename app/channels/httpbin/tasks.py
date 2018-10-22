from app.core.tasks import BaseTaskHandler
from django.conf import settings
from utils.requests import requests


class HTTPBINDummyNotificationTaskHandler(BaseTaskHandler):
    """
    HTTPBIN send dummy notification task handler
    """
    name = 'httpbin.dummy.send_message'
    state_transition = True
    support_recon = True
    operation_tag = 'send_dummy_notification'

    def execute(self, params):
        url = '{0}/{1}'.format(settings.HTTPBIN_URL, "post")
        results = requests.post(
            url,
            data=dict(recipients=params.recipients, message=params.message)
        )
        self.message_obj.data['status']['results'] = dict(
            status_code=results.status_code,
            data=results.json()
        )
        return results
