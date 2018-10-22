# import package
import africastalking


class AfricasTalkingClient:
    """

    """
    def __init__(self, username, api_key):
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS

    def send_message(self, recipients, message, sender=None, callback=None):
        if not isinstance(recipients, list):
            raise TypeError(
                "`recipients` expected to be a `list` but `{0}` found".format(
                    type(recipients)
                )
            )
        return self.sms.send(
            message, recipients, sender_id=sender, callback=callback
        )
