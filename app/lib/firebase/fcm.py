import firebase_admin
from firebase_admin import credentials, messaging


file_path = './pycon-monitoring-workshop-firebase-adminsdk.json'
cred = credentials.Certificate(file_path)
default_app = firebase_admin.initialize_app(cred)


def send_message(recipients, message, dry_run=False):
    if not isinstance(recipients, list):
        raise TypeError(
            "`recipients` expected to be a `list` but `{0}` found".format(
                type(recipients)
            )
        )
    for registration_token in recipients:
        message = messaging.Message(
            data=dict(message=message),
            token=registration_token,
        )
    return messaging.send(message, dry_run)
