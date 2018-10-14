import copy
from six import with_metaclass
from configuration.celery import app
from django.conf import settings
from django.utils import timezone
from .models import MessageRequest
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

    event_name = None

    logger = get_logger(__name__)

    def __init__(self):
        self.kwargs = dict()
        self.message_obj = None
        self.message_id = None
        self.channel = None
        self.message_type = None

    def initiate(self, message_id):
        self.message_id = message_id
        self.message_obj = MessageRequest.objects.get_latest_message(
            message_id=self.message_id
        )
        self.channel = self.message_obj.data.get('channel')
        self.message_type = self.message_obj.data.get('message_type')

    def _state_transition(self):
        self.logger.debug("state_transition_kwargs", kwargs=self.kwargs)
        return self.kwargs.get('state_transition') \
            if 'state_transition' in self.kwargs \
            else self.state_transition

    def change_state(self, state):
        try:
            if self._state_transition():
                previous_state = self.message_obj.state
                if state == MessageRequest.received:
                    self.message_obj.started()
                elif state == MessageRequest.completed:
                    self.message_obj.completed()
                self.message_obj.save()
                self.logger.info("state_transition",
                                 from_=previous_state,
                                 to=self.message_obj.state)
        except Exception as err:
            self.logger.error("state_transition_error", error=str(err))
            raise err

    def transition_to_in_progress(self):
        # self.change_state(ApiRequest.in_progress)
        pass

    def transition_to_complete(self):
        # self.change_state(ApiRequest.completed)
        pass

    def run(self, message_id, *args, **kwargs):
        assert message_id, "message_id should be defined"
        self.initiate(message_id)
        self.kwargs = copy.deepcopy(kwargs)
        self.event_name = self.event_name or self.message_obj.message_type
        recon = self.message_obj.data.get('recon', False)
        processed_calling_task_run_method = True
        if recon:
            if self.support_recon and hasattr(self, 'handle_recon'):
                processed_calling_task_run_method = self.handle_recon()

        # add self if this is a bound task
        if processed_calling_task_run_method:
            if self._state_transition():
                self.transition_to_in_progress()

            results = self.handler(*args, **kwargs)
            if self._state_transition():
                self.transition_to_complete()
        else:
            self.logger.info("invalid_state")
            results = self.message_id
        return results

    def handler(self, *args, **kwargs):
        try:
            self.logger.info("{}_task_start".format(self.event_name))
            response = self.execute(
                MessageDataParser(
                    self.message_id,
                    **self.message_obj.data
                )
            )
            self.logger.info("execute_response", **response)
            self.logger.info("{}_task_end".format(self.event_name), **response)
        except Exception as e:
            self.logger.error(
                '{}_task_end'.format(self.event_name),
                error=str(e),
                **self.message_obj.data.get('callback', {})
            )
        return self.message_id

    def get_diff_time(self):
        delta = timezone.now() - self.message_obj.createdAt
        return delta.total_seconds()

    def handle_recon(self):
        recon_time = settings.DEFAULT_RECON_TIME_IN_MINUTES
        if self.message_obj.state == MessageRequest.received and \
                float(self.get_diff_time()) < float(recon_time * 60):
            return True
        return False

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
    event_name = 'send_message_callback'

    def execute(self, params):
        self.logger.info(event='{}_start'.format(self.event_name))
        return dict()
