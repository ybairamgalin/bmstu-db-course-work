import logging

from starlette.responses import Response

from task_tracker_backend import models

from task_tracker_backend.pg.task.get import get_task_id_by_public_id
from task_tracker_backend.pg.comment.save import save_comment


async def task_comment_add_post(
        public_id: str,
        body: models.CommentAddPostRequestBody,
        auth_token: models.Token,
):
    try:
        task_id = get_task_id_by_public_id(public_id)
    except RuntimeError as error:
        logging.warning(error)
        return Response('Неверный идентификатор задачи', status_code=400)
    save_comment(body.text, task_id, auth_token.user_id)
    return Response(status_code=201)
