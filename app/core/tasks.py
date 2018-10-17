import copy
from six import with_metaclass
from configuration.celery import app
from .models import MessageRequest, FSMStates
from .parsers import MessageDataParser
from utils.logging import get_logger


class TaskMetaClass(type):
    """
    Metaclass to register celery tasks in the task registry.

    As of celery 4.0.1, the task class is no longer using a special meta-class
    that automatically registers the task in the task registry hence the need
    for this metaclass.
    """
    def __init__(cls, name, bases, attr):
        super(TaskMetaClass, cls).__init__(name, bases, attr)
        if not attr.get('abstract', False):
            app.register_task(cls())


class BaseTaskHandler(with_metaclass(TaskMetaClass, app.Task)):
    """
    Base task handler class forming the core tasks workflow class.

    Any class that inherits from this class is automatically registered to
    Celery's task registry as long as it's not abstract.

    It initiates this class with instance of MessageRequest

    Children classes subclassing this class are expected to:
        - define an `execute` method, to be called with a `message_id` &
        all the args provided by the view calling this task
    """
    abstract = True

    state_transition = True

    support_recon = True

    operation_tag = None

    def __init__(self):
        self.kwargs = dict()
        self.message_obj = None
        self.message_id = None
        self.channel = None
        self.message_type = None
        self.logger = None

    def initiate(self, message_id):
        self.message_id = message_id
        self.message_obj = MessageRequest.objects.get_latest_message(
            message_id=self.message_id
        )
        self.channel = self.message_obj.data.get('channel')
        self.message_type = self.message_obj.data.get('message_type')
        self.logger = get_logger(__name__).bind(
            operation="{0}_task".format(self.operation),
            message_id=self.message_id,
            **self.message_obj.data
        )

    def run(self, message_id, *args, **kwargs):
        assert message_id, "message_id should be defined"
        self.initiate(message_id)
        self.kwargs = copy.deepcopy(kwargs)
        return self.task_handler(*args, **kwargs)

    def task_handler(self, *args, **kwargs):
        try:
            self.logger.info(event="start")
            if self.transitions_allowed:
                self._transition_state(FSMStates.STARTED.value)
            response = self.execute(
                MessageDataParser(
                    self.message_id,
                    **self.message_obj.data
                )
            )
            self.logger.info(event="end", **response)
            if self.transitions_allowed:
                self._transition_state(FSMStates.SUBMITTED.value)
        except Exception as e:
            self.logger.error(
                event="error",
                error=str(e),
                **self.message_obj.data.get('callback', {})
            )
            if self.transitions_allowed:
                self._transition_state(FSMStates.SUBMITTED.value)
        return self.message_id

    def _transition_state(self, target):
        tag = "state_trasition"
        try:
            current = previous = self.message_obj.state
            self.logger.info(
                event="{0}_start".format(tag),
                message_id=self.message_obj.message_id,
                current_state=current,
                target_state=target
            )
            getattr(self.message_obj, target)()
            self.message_obj.save()
            self.logger.info(
                event="{0}_end".format(tag),
                message_id=self.message_obj.message_id,
                previous_state=previous,
                new_state=self.message_obj.state
            )
        except Exception as e:
            self.logger.error(
                event="{0}_error".format(tag),
                message_id=self.message_obj.message_id,
                error=e.__class__.__name__,
                error_message=str(e)
            )
            raise e

    def _update_attempts(self):
        self.message_obj.data.update(
            dict(attempts=self.message_obj.data.get('attempts', 0)+1)
        )
        self.message_obj.save()

    @property
    def operation(self):
        return self.operation_tag or \
               "{0}_{1}".format(self.channel, self.message_type)

    @property
    def transitions_allowed(self):
        return self.kwargs.get('state_transition') \
            if 'state_transition' in self.kwargs.keys() \
            else self.state_transition

    def execute(self, params):
        raise NotImplementedError(
            "`execute` method has not been implemented"
        )


class SendMessageCallbackHandler(BaseTaskHandler):
    """
    Send message task callback handler
    """
    name = 'all.send_message.callback'
    queue = 'all.send_message.callback'
    state_transition = False
    support_recon = True
    operation_tag = 'send_message_callback'

    def execute(self, params):
        self._transition_state(FSMStates.DELIVERED.value)
        return dict()
