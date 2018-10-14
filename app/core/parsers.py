"""
Module containing classes that parses data from one format to another.
"""
import copy


class MessageDataParser(object):
    """
    Create an object with request params set as attributes in an instance of
    this class
    """
    def __init__(self, message_id, **kwargs):
        self.message_id = message_id

        for key, value in list(kwargs.items()):
            setattr(self, key, value)

    def all_params(self):
        return copy.deepcopy(self.__dict__)
