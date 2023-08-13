import datetime as dt

from starlette.responses import Response

from task_tracker_backend import clickhouse
from task_tracker_backend.kafka import Producer


async def audit_import_tasks_post():
    msg = f'{dt.datetime.now()}'
    Producer.write_flush('tasks_history', msg.encode('utf-8'))

    # data = clickhouse.Clickhouse.retrieve(
    #     'select value_before, updated_at '
    #     'from tasks_history '
    #     'where task_id=1'
    # )
    # print(data)
    return Response(status_code=200)
