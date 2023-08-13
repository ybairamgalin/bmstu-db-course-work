import logging
import sys

from task_tracker_backend import models


def setup_logging(level=logging.INFO):
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
    root_logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    logging.basicConfig(
        filename=models.Config.get_item('logging')['logs_file_path'],
    )
