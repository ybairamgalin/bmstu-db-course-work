import clickhouse_connect


class Clickhouse:
    __client = None

    def __init__(self):
        raise RuntimeError('Constructor should not be called')

    @staticmethod
    def open_connection(credentials):
        Clickhouse.__client = clickhouse_connect.get_client(
            host=credentials['host'], port=credentials['port']
        )

    @staticmethod
    def command(query):
        Clickhouse.__client.command(query)

    @staticmethod
    def retrieve(query, args=None):
        result = Clickhouse.__client.query(query, parameters=args)
        return result.result_rows

    @staticmethod
    def batch_insert(table, data, columns):
        Clickhouse.__client.insert(table, data, columns)
