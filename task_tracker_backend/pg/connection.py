import logging

import psycopg2


class Pg:
    __connection = None
    __credentials = None

    def __init__(self):
        raise RuntimeError('Constructor should not be called')

    @staticmethod
    def open_connection(credentials):
        Pg.__credentials = credentials
        Pg.__init_connection()

    @staticmethod
    def execute_no_return(query, args=()):
        try:
            cursor = Pg.__connection.cursor()
            cursor.execute(query, args)
            Pg.__connection.commit()
        except Exception as error:
            logging.error('database exception: %s', error)
            Pg.__connection.rollback()
            raise error

    @staticmethod
    def execute(query, args=()):
        try:
            cursor = Pg.__connection.cursor()
            cursor.execute(query, args)
            Pg.__connection.commit()
            return cursor.fetchall()
        except Exception as error:
            logging.error('database exception: %s', error)
            Pg.__connection.rollback()
            raise error

    @staticmethod
    def __init_connection():
        Pg.__connection = psycopg2.connect(
            database=Pg.__credentials['database'],
            user=Pg.__credentials['user'],
            password=Pg.__credentials['password'],
            host=Pg.__credentials['host'],
            port=Pg.__credentials['port'],
        )
