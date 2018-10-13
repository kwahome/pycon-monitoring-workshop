from django.db import models
from django.db.transaction import atomic


class MessageManager(models.Manager):

    """
    Used select_for_update() as it locks the resultant query set until the end
    of the transaction, this will eliminate the errors (TransitionNotAllowed)
    that may occur when when two state transitions are attempted simultaneously
    """

    def get_latest_message(self, message_id):
        with atomic():
            return self.select_for_update().filter(
                messageId=message_id
            ).exclude(
                createdAt=None
            ).latest('createdAt')
