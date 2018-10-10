import logging
import os


# from .celeryapp import app as celery_app

# __all__ = ['celery_app']


class CustomFilter(logging.Filter):

    def __init__(self):
        self.environment = os.environ["ENVIRONMENT"]
        self.supervisor_process_name = os.environ.get("SUPERVISOR_PROCESS_NAME")
        super(CustomFilter, self).__init__()

    def filter(self, record):
        record.environment = self.environment
        record.supervisor_process_name = self.supervisor_process_name
        return True
