import asyncio
import logging
import sys
import json
import datetime as dt

import clickhouse_connect
from kafka import TopicPartition
from kafka import KafkaConsumer

TASKS_HISTORY_TABLE = 'tasks_history'
TASKS_HISTORY_TOPIC = 'tasks_history'
CLICK_COLUMNS = [
    'task_id',
    'field',
    'value_before',
    'value_after',
    'updated_by',
    'updated_at'
]

def main():
    set_logger()
    logging.info('Tasks history transfer started')
    asyncio.run(tasks_history_transfer())


def set_logger(level=logging.INFO):
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
    root_logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def make_consumer():
    return KafkaConsumer(
        TASKS_HISTORY_TOPIC,
        bootstrap_servers=[
            'kafka_service:29092'
        ],
        auto_offset_reset='earliest',
        group_id='1',
    )


def make_clickhouse_connection():
    return clickhouse_connect.get_client(
        host='clickhouse_server', port=8123
    )


async def tasks_history_transfer():
    consumer = make_consumer()
    clickhouse = make_clickhouse_connection()
    while True:
        logging.info('Started to read new batch')
        messages = consumer.poll(5, 1500)
        consumer.commit()
        click_data = []
        if messages:
            topic_partition = TopicPartition(topic=TASKS_HISTORY_TOPIC, partition=0)
            for consumer_record in messages[topic_partition]:
                record_dict = json.loads(consumer_record.value.decode('utf-8'))
                click_data.append(
                    [
                        record_dict['task_id'],
                        record_dict['field'],
                        record_dict['value_before'],
                        record_dict['value_after'],
                        record_dict['updated_by'],
                        dt.datetime.fromisoformat(record_dict['updated_at']),
                    ]
                )
            clickhouse.insert(
                TASKS_HISTORY_TABLE, click_data, CLICK_COLUMNS,
            )

        await asyncio.sleep(10)


if __name__ == '__main__':
    main()
