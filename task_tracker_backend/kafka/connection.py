from kafka import KafkaProducer
from kafka import KafkaConsumer


class Producer:
    __connection = None
    __credentials = None

    def __init__(self):
        raise RuntimeError('Constructor should not be called')

    @staticmethod
    def open_connection(credentials):
        Producer.__credentials = credentials
        Producer.__init_connection()

    @staticmethod
    def write_flush(topic: str, msg: bytes):
        future = Producer.__connection.send(topic, msg)
        result = future.get(5)
        print(result)
        Producer.__connection.flush()

    @staticmethod
    def __init_connection():
        print('IAROSLAV ', Producer.__credentials["host"])
        print('IAROSLAV ', Producer.__credentials["port"])
        Producer.__connection = KafkaProducer(
            bootstrap_servers=[
                f'{Producer.__credentials["host"]}:'
                f'{Producer.__credentials["port"]}'
            ],
        )


class Consumer:
    __topic_to_connection = dict()
    __topic_to_credentials = dict()

    def __init(self):
        raise RuntimeError('Constructor should not be called')

    @staticmethod
    def open_connection(topic: str, credentials):
        Consumer.__topic_to_credentials[topic] = credentials

    @staticmethod
    def read(topic):
        if topic not in Consumer.__topic_to_connection:
            raise RuntimeError(
                f'Connection to {topic} was not established before '
                'read attempt'
            )

        return next(Consumer.__topic_to_connection[topic])

    @staticmethod
    def __init_connection(topic: str):
        Consumer.__topic_to_connection[topic] = KafkaConsumer(
            topic, bootstrap_servers=[
                f'{Consumer.__topic_to_credentials[topic]["host"]}:'
                f'{Consumer.__topic_to_credentials[topic]["port"]}'
            ]
        )
