from django.db import models
from django_fsm import FSMField, transition
from enum import Enum
from jsonfield import JSONField
from .managers import MessageManager


# Define State Machine
received, started, failed, submitted, completed = (
    "received",
    "started",
    "failed",
    "submitted",
    "completed",
)


class ChoicesEnum(Enum):
    @classmethod
    def yield_choices(cls):
        return tuple((x.value, x.name) for x in cls)


class MessageTypes(ChoicesEnum):
    PUSH = 'push'
    SMS = 'sms'


class MessageChannels(ChoicesEnum):
    AT = 'africa-is-talking'
    FIREBASE = 'firebase'
    SMPP = 'smpp'


class FSMChoices(ChoicesEnum):
    RECEIVED = received
    STARTED = started
    FAILED = failed
    SUBMITTED = submitted
    COMPLETED = completed


class BaseModel(models.Model):
    """
    Base data model for all objects
    Defines `__repr__` & `json` methods or any common method that you need
    for all your models
    """
    received, started, failed, submitted, completed = (
        received, started, failed, submitted, completed
    )

    class Meta:
        abstract = True

    state = FSMField(
        default=received,
        choices=FSMChoices.yield_choices(),
        protected=True,
        db_index=True
    )

    @transition(field=state, source=[received, failed], target=started)
    def started(self):
        """
        Change message request to `started` state.
        """
        return

    @transition(field=state, source="*", target=failed)
    def failed(self):
        """
        For requests in `started` that cannot be submitted to Network
        hence in the `failed` state.
        """
        return

    @transition(
        field=state,
        source=[submitted, failed, completed],
        target=completed,
    )
    def completed(self):
        """
        Request was successfully `submitted` to message center/server and a
        response returned.

        Can also transition from source=completed to accommodate delivery
        notifications from message center/server even after the task has
        been `completed`
        """
        return

    @transition(field=state, source=started, target=submitted)
    def submitted(self):
        """
        Change message request to `submitted` state.
        """
        return


class MessageRequest(BaseModel):
    class Meta:
        db_table = "message"

    message_id = models.CharField(
        max_length=255,
        db_index=True
    )
    data = JSONField(
        default=dict(attempts=0)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()
