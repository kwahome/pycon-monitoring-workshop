import datetime
import functools
import structlog
import time
from .processors import KeyValueRenderer


def init_logging():
    # configure structlog
    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=structlog.threadlocal.wrap_dict(dict),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.UnicodeEncoder(),
            KeyValueRenderer(),
        ]
    )


get_logger = structlog.get_logger


def with_logger(name='', **logger_kwargs):
    """
    Wrapper to log before and after function calls.

    :param name: name to initialize the logger with
    :param kwargs: key-word arguments of thing to bind in the logger
    :return:
    """
    tag = "network_request"

    def wrapper(func):
        @functools.wraps(func)
        def inner(*f_args, **f_kwargs):
            logger = get_logger(name)
            response = error = None
            start = time.time()
            logger.info(
                event="{0}_start".format(tag),
                arguments=f_args,
                **f_kwargs,
                start_time=datetime.datetime.now().isoformat()
            )
            try:
                response = func(*f_args, **f_kwargs)
            except Exception as e:
                error = e
            finally:
                duration = (time.time() - start) * 1000
                logger.info(
                    event="{0}_end".format(tag),
                    arguments=f_args,
                    **f_kwargs,
                    error=error,
                    end_time=datetime.datetime.now().isoformat(),
                    duration="{0}ms".format(duration)
                )
                if error:
                    raise error
            return response
        return inner
    return wrapper
