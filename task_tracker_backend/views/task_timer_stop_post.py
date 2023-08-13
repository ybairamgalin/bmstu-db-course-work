import logging

from starlette.responses import Response

from task_tracker_backend import models

from task_tracker_backend.pg.timer.save import stop_task_timer
from task_tracker_backend.pg.task.get import get_task_id_by_public_id
from task_tracker_backend.pg.task.save import increase_task_spent_time


async def task_timer_stop_post(public_id: str, auth_token: models.Token):
    try:
        task_id = get_task_id_by_public_id(public_id)
        spent_time = stop_task_timer(task_id, auth_token.user_id)
        increase_task_spent_time(spent_time, task_id)
        return Response(status_code=200)
    except RuntimeError as error:
        logging.warning(error)
        return Response(status_code=400)
