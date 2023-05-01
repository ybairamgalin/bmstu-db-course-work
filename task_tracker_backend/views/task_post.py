from typing import Union

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.save import save_task_returning_id


def to_models_task(
        user_request: models.TaskPostRequestBody, user_id: int,
):
    return models.Task(
        title=user_request.title,
        content=user_request.content,
        creator_id=user_id
    )


async def task_post(
        request: models.TaskPostRequestBody,
        token: models.Token,
        dependencies: models.Dependencies,
):
    task = to_models_task(request, token.user_id)

    try:
        task_id = save_task_returning_id(task, dependencies)
    except RuntimeError:
        return Response(
            utils.to_json({'message': 'Could not create task'}),
            status_code=401,
        )
    return Response(utils.to_json({'id': task_id}), status_code=201)
