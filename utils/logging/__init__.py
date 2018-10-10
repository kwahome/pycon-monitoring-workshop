import structlog
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
