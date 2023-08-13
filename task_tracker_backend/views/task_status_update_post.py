import logging
import datetime as dt

from starlette.responses import Response

from task_tracker_backend import models

from task_tracker_backend.pg.task.save import save_task_status
from task_tracker_backend.pg.task.get import get_task_by_public_id
from task_tracker_backend.kafka.task_change import send_task_change


async def task_status_update_post(
        public_id: str,
        body: models.TaskStatusUpdatePostRequestBody,
        auth_token: models.Token,
):
    try:
        task = get_task_by_public_id(public_id)
    except RuntimeError as error:
        logging.info(error)
        return Response(status_code=404)
    if task.status.value == body.new_status.value:
        logging.info('Task status is the same as before')
        return Response(status_code=400)
    try:
        save_task_status(public_id, body.new_status)
    except RuntimeError as error:
        logging.warning(error)
        return Response(status_code=400)
    send_task_change(
        models.TaskChange(
            task_id=task.public_id,
            field=models.TaskField.STATUS,
            value_before=task.status.value,
            value_after=body.new_status.value,
            updated_by=auth_token.username
            if auth_token.username
            else 'undefined',
            updated_at=dt.datetime.now().isoformat()
        )
    )

    return Response(status_code=200)
