import functools
import time
import threading
from .metrics import SimpleMetrics, Constants


def metrics():
    thread = threading.current_thread()
    container = getattr(thread, Constants.METRICS, None)
    if container is None:
        container = SimpleMetrics()
        setattr(thread, Constants.METRICS, container)
    return container


def timer(name='timer', **ctx_kwargs):
    """
    Time-measuring decorator: the time spent in the wrapped block is measured
    and added to the named metric.

    :param name:
    :param ctx_kwargs:
    :return:
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*f_args, **f_kwargs):
            _metrics = metrics()
            _metrics.context(ctx_kwargs)
            response = error = None
            start = time.time()
            try:
                response = func(*f_args, **f_kwargs)
            except Exception as e:
                error = e
            finally:
                end = time.time()
                duration = (end - start) * 1000
                _metrics.time(name, duration)
                if error is not None:
                    _metrics.error(error)
                    raise error
            return response
        return inner
    return wrapper
