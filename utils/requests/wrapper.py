"""
Wrapper around requests library APIs
"""
import requests
from utils.logging import with_logger


class RequestsWrapper(object):
    """
    Wrapper around Python's requests package APIs for custom functionality
    mostly geared towards tracing and logging.

    Overriding `__getattr__` which will be called if `__getattribute__` (called
    for all attribute lookups in this class) fails with an `AttributeError`
    makes it possible to do an attribute lookup from the `requests` library and
    wrap the attribute if found.
    """
    def __init__(self):
        self._wrapper = with_logger(__name__)

    @property
    def wrapper(self):
        return self._wrapper

    @wrapper.setter
    def wrapper(self, wrapper=None):
        self._wrapper = wrapper

    def __getattr__(self, attr):
        r"""Returns a wrapped attribute `attr` of the requests API.
        """
        _attr = getattr(requests, attr)
        return self.wrapper(_attr) if self.wrapper else _attr
