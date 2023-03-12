import dataclasses

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.get import get_task_by_id


async def task_get(task_id: int, dependencies: models.Dependencies):
    try:
        task = get_task_by_id(task_id, dependencies)
        return Response(utils.to_json(
            {"task": dataclasses.asdict(task)}), status_code=200
        )
    except RuntimeError as error:
        return Response(utils.to_json(
            {'message': str(error)}),
            status_code=404
        )
