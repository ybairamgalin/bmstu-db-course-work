import dataclasses

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.get import get_task_by_id


async def task_get(body: dict, dependencies: models.Dependencies):
    if 'task_id' not in body:
        raise RuntimeError('No task id')
    task = get_task_by_id(body['task_id'], dependencies)
    return Response(utils.to_json(
        {"task": dataclasses.asdict(task)}), status_code=200
    )
