import configparser

from task_tracker_backend import constants
from task_tracker_backend import pg


class Dependencies(object):
    def __init__(self):
        self.config = _init_config()
        print(self.config.items())
        self.pg = pg.Pg(self.config['postgres'])


def _init_config():
    config = configparser.ConfigParser()
    config.read(constants.CONFIG_FILE)
    return config
