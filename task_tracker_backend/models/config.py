import configparser

from task_tracker_backend import constants


class Config:
    __config = None

    def __init__(self):
        raise RuntimeError('Constructor should not be called')

    @staticmethod
    def load_config():
        Config.__init_config()

    @staticmethod
    def get_item(name: str):
        return Config.__config[name]

    @staticmethod
    def __init_config():
        Config.__config = configparser.ConfigParser()
        Config.__config.read(constants.CONFIG_FILE)
