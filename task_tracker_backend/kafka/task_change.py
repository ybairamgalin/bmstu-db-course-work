import json

from task_tracker_backend import models
from task_tracker_backend.kafka.connection import Producer

TASKS_HISTORY_TOPIC = 'tasks_history'


def send_task_change(task_change: models.TaskChange):
    msg = task_change.json()
    Producer.write_flush(TASKS_HISTORY_TOPIC, msg.encode('utf-8'))

