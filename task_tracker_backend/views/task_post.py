from typing import Union

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.save import save_task_returning_id


def to_models_task(
        user_request: models.TaskPostRequestBody,
        user_id_str: str,
):
    try:
        user_id = int(user_id_str)
    except ValueError as error:
        raise RuntimeError('Bad user id') from error

    return models.Task(
        title=user_request.title,
        content=user_request.content,
        creator_id=user_id
    )


async def task_post(
        request: models.TaskPostRequestBody,
        x_user_id: Union[str, None],
        dependencies: models.Dependencies,
):
    if not x_user_id:
        return Response(
            utils.to_json({'message': 'Missing X-User-Id header'}),
            status_code=401,
        )

    try:
        task = to_models_task(request, x_user_id)
    except RuntimeError:
        return Response(
            utils.to_json({'message': 'Bad user id'}),
            status_code=401,
        )

    try:
        task_id = save_task_returning_id(task, dependencies)
    except RuntimeError:
        return Response(
            utils.to_json({'message': 'Could not create task'}),
            status_code=401,
        )
    return Response(utils.to_json({'id': task_id}), status_code=201)
