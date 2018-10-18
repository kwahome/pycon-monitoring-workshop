from django.db import models
from django_fsm import FSMField, transition
from enum import Enum
from jsonfield import JSONField
from .managers import MessageManager


_received, _started, _failed, _submitted, _delivered = (
    "received",
    "started",
    "failed",
    "submitted",
    "delivered",
)


class ChoicesEnum(Enum):
    @classmethod
    def yield_choices(cls):
        return tuple((x.value, x.name) for x in cls)


class MessageTypes(ChoicesEnum):
    PUSH = 'push'
    SMS = 'sms'


class MessageChannels(ChoicesEnum):
    AT = 'africas-talking'
    FIREBASE = 'firebase'
    SMPP = 'smpp'


class FSMStates(ChoicesEnum):
    """
    Class that exposes possible FSM states with methods to yield a tuple
    of those states as choices.

    Also, to access the string values of the states, use FSMStates.<STATE>.value
    """
    RECEIVED = _received
    STARTED = _started
    FAILED = _failed
    SUBMITTED = _submitted
    DELIVERED = _delivered


class BaseModel(models.Model):
    """
    Base data model for all objects
    Defines `__repr__` & `json` methods or any common method that you need
    for all your models
    """

    class Meta:
        abstract = True

    state = FSMField(
        default=_received,
        choices=FSMStates.yield_choices(),
        protected=True,
        db_index=True
    )

    @transition(
        field=state,
        source=[_received, _failed],
        target=_started
    )
    def started(self):
        """
        Change message request to `started` state.
        """
        return

    @transition(
        field=state,
        source="*",
        target=_failed
    )
    def failed(self):
        """
        For requests in `started` that cannot be submitted to Network
        hence in the `failed` state.
        """
        return

    @transition(
        field=state,
        source=_started,
        target=_submitted
    )
    def submitted(self):
        """
        Change message request to `submitted` state from `started` state.
        """
        return

    @transition(
        field=state,
        source=[_submitted, _failed, _delivered],
        target=_delivered
    )
    def delivered(self):
        """
        Request was successfully `submitted` to message center/server and a
        response returned.

        Can also transition from source=`delivered` to accommodate for delivery
        notifications from message center/server even after the task has
        been `delivered`
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
        default=dict(status=dict(attempts=0))
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()
