import psycopg2


class Pg:
    def __init__(self, credentials):
        self.connection = psycopg2.connect(
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
            host=credentials['host'],
            port=credentials['port'],
        )

    def execute_no_return(self, query, args=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            raise error

    def execute(self, query, args=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as error:
            self.connection.rollback()
            raise error
