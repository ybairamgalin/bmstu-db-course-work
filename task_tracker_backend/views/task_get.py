from starlette.responses import Response

from task_tracker_backend import utils
from task_tracker_backend.pg.task.get import get_task_by_public_id


async def task_get(public_id: str):
    try:
        task = get_task_by_public_id(public_id)
        return task
    except RuntimeError as error:
        return Response(utils.to_json(
            {'message': str(error)}),
            status_code=404
        )
