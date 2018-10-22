import asyncio
from app.core.tasks import BaseTaskHandler
from app.lib.smpp.naz_client import OutboundQueue


class SMPPSendMessageTaskHandler(BaseTaskHandler):
    """
    SMPP send message task handler
    """
    name = 'smpp.sms.send_message'
    state_transition = False
    support_recon = True
    operation_tag = 'send_smpp_message'

    def execute(self, params):
        loop = asyncio.get_event_loop()
        for recipient in params.recipients:
            payload = {
                "smpp_event": "submit_sm",
                "short_message": params.message,
                "correlation_id": self.message_id,
                "source_addr": params.sender_id,
                "destination_addr": recipient,
            }
            self.logger.info(
                event="smpp_outbound_enqueueing",
                smpp_payload=payload,
                smpp_outbound_queue=OutboundQueue.__class__.__name__
            )
            loop.run_until_complete(OutboundQueue.enqueue(payload))
        results = dict(enqueued=True)
        self.message_obj.data['status']['results'] = results
        return results
