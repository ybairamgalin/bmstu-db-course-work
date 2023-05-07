import logging

from task_tracker_backend import models

LOG_FORMAT = '%(asctime)s level=%(levelname)s file=%(filename)s' \
             ' function=%(funcName)s text=\'%(message)s\''


def setup_logging():
    logging.basicConfig(
        filename=models.Config.get_item('logging')['logs_file_path'],
        format=LOG_FORMAT,
    )
