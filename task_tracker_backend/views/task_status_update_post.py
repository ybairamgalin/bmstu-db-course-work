import logging

from starlette.responses import Response

from task_tracker_backend import models

from task_tracker_backend.pg.task.save import save_task_status


async def task_status_update_post(
        public_id: str,
        body: models.TaskStatusUpdatePostRequestBody
):
    try:
        save_task_status(public_id, body.new_status)
    except RuntimeError as error:
        logging.warning(error)
        return Response(status_code=400)

    return Response(status_code=200)
