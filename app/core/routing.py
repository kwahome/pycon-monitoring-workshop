"""
Defines logic used to route message requests to the appropriate handlers
"""
from six import with_metaclass
from .exceptions import MissingAttributeException, InvalidAttributeException
from .models import MessageTypes
from utils.logging import get_logger

logger = get_logger(__name__)


ROUTING_REGISTRY = dict()


class RoutingHandlerMetaClass(type):
    """
    Metaclass to register message handler upon creation
    """
    _required_attrs_ = ('channel', 'message_type', 'route_task')

    _attr_types_ = dict(
        channel=str,
        message_type=str
    )

    def __init__(cls, name, bases, attr):
        super(RoutingHandlerMetaClass, cls).__init__(name, bases, attr)
        if hasattr(cls, 'message_type'):
            attr['message_type'] = cls.message_type
        cls.name = name
        cls.attr = attr
        if not cls.attr.get('abstract', False):
            cls._validate_required_attr()
            cls._validate_attr_types()
            cls._register()

    def _validate_required_attr(cls):
        # check all attributes have been defined
        for attr in cls._required_attrs_:
            if attr not in cls.attr and not hasattr(cls, attr):
                raise MissingAttributeException(
                    "{0} is a required attribute in class {1}".format(
                        attr, cls.name
                    )
                )

    def _validate_attr_types(cls):
        for attr, _type in cls._attr_types_.items():
            if type(cls.attr[attr]) is not _type:
                raise InvalidAttributeException(
                    """Attribute {0} of class {1} expected to be of type {2}
                    but {3} found""".format(
                        attr, cls.name, _type, type(attr)
                    )
                )

    def _register(cls):
        if not ROUTING_REGISTRY.get(cls.attr['message_type']):
            ROUTING_REGISTRY[cls.attr['message_type']] = {
                cls.attr['channel']: cls
            }
        else:
            if ROUTING_REGISTRY[cls.attr['message_type']].get(
                    cls.attr['channel']
            ):
                raise IndexError(
                    """A handler of message_type=`{0}` for channel=`{1}` 
                    has already been registered""".format(
                        cls.attr['message_type'], cls.attr['channel']
                    ))
            ROUTING_REGISTRY[cls.attr['message_type']].update(
                {cls.attr['channel']: cls}
            )


class RoutingAbstractHandler(with_metaclass(RoutingHandlerMetaClass, object)):
    """
     - Any object inheriting this object is expected to have the following
     attributes:
        1. channel
        2. message_type
        3. route_task

     - Any object inheriting this object should be registered in
        ROUTING_REGISTRY with the `channel` as the key

    - An instance of this class is initialized with a `message_obj`
    """
    abstract = True

    def __init__(self, message_obj):
        self.message_obj = message_obj


class SMSAbstractRoutingHandler(RoutingAbstractHandler):
    """
    Abstract `sms` routing handler
    """
    abstract = True
    message_type = MessageTypes.SMS.value


class PushNotificationAbstractRoutingHandler(RoutingAbstractHandler):
    """
    Abstract `push` notification routing handler
    """
    abstract = True
    message_type = MessageTypes.SMS.value
