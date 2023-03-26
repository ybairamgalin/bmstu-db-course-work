import dataclasses
import datetime as dt

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.get import get_tasks


async def task_info_post(
        request: models.TaskInfoPostRequestBody,
        dependencies: models.Dependencies,
):
    db_tasks = get_tasks(request.name_part, dt.datetime.now(), 10, dependencies)

    response = {'tasks': list()}
    for task in db_tasks:
        response['tasks'].append(task)

    return Response(utils.to_json(response), status_code=200)
