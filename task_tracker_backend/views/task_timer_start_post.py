import logging

from starlette.responses import Response

from task_tracker_backend import models

from task_tracker_backend.pg.task.get import get_task_id_by_public_id
from task_tracker_backend.pg.timer.save import start_task_timer


async def task_timer_start_post(public_id: str, auth_token: models.Token):
    try:
        task_id = get_task_id_by_public_id(public_id)
        start_task_timer(task_id, auth_token.user_id)
        return Response(status_code=200)
    except RuntimeError as error:
        logging.warning(error)
        return Response(status_code=400)
