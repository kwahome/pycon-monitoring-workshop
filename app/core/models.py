from django.db import models
from django_fsm import FSMField, transition
from enum import Enum


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
    GOOGLE = 'google'
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
    class Meta:
        abstract = True

    state = FSMField(
        default=received, choices=FSMChoices.yield_choices(), protected=True
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


class MessageModel(BaseModel):
    class Meta:
        db_table = "message"

    messageId = models.CharField(max_length=64, unique=True)
    senderId = models.CharField(max_length=64)
    recipientId = models.CharField(max_length=64)
    messageType = models.CharField(
        max_length=64, choices=MessageTypes.yield_choices()
    )
    channel = models.CharField(
        max_length=64, choices=MessageChannels.yield_choices()
    )
    message = models.CharField(max_length=200)
    priority = models.CharField(
        max_length=64, default="normal", blank=True, null=True
    )
    status = models.CharField(max_length=64, default="")
    callback = models.CharField(max_length=200, default="")
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
