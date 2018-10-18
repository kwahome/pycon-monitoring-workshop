"""
Module containing classes that parses data from one format to another.
"""
import copy
import json


class BaseDataParser(object):
    """
    Base data parser
    """
    def all_params(self):
        return copy.deepcopy(self.__dict__)

    def to_json(self):
        return json.dumps(self.all_params())


class MessageDataParser(BaseDataParser):
    """
    Create an object with request params set as attributes in an instance of
    this class
    """
    def __init__(self, message_id, **kwargs):
        self.message_id = message_id

        for key, value in list(kwargs.items()):
            # split comma separated string of recipients into a list
            value = value.split(",") if key is "recipients" else value
            setattr(self, key, value)


class CallbackDataParser(BaseDataParser):
    """
    Create an object with results of a send message operation set as attributes
    in an instance of this class.

    Also provides methods to serialize params into a `json` type that can be
    transmitted over the wire.
    """

    def __init__(self, message_id, delivery_status, **kwargs):
        self.message_id = message_id
        self.delivery_status = delivery_status

        for key, value in list(kwargs.items()):
            setattr(self, key, value)

