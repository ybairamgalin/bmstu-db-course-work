from typing import Union
from typing import List

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils

from task_tracker_backend.pg.task.save import save_task_returning_id
from task_tracker_backend.pg.task.save import save_task_tags
from task_tracker_backend.pg.tag.save import save_tags_returning_ids
from task_tracker_backend.pg.tag.get import get_tags_by_values


def parse_tags(tags_string: Union[str, None]):
    if tags_string is None:
        return list()

    return [tag.strip() for tag in tags_string.split(',')]


def convert_to_models_task(
        user_request: models.TaskPostRequestBody, user_id: int,
):
    return models.Task(
        title=user_request.title,
        content=user_request.content,
        creator_id=user_id,
        tags=parse_tags(user_request.tags),
    )


def get_tags_to_insert(new_tags: List[str], existing_tags: set[str]):
    tags_to_insert = list()
    for tag in new_tags:
        if tag in existing_tags:
            continue

        tags_to_insert.append(tag)

    return tags_to_insert


def merge_tags(tags, dependencies: models.Dependencies):
    existing_tags = get_tags_by_values(tags, dependencies)

    existing_tags_values = {tag.value for tag in existing_tags}
    tags_to_insert = get_tags_to_insert(tags, existing_tags_values)

    new_tag_ids = set(save_tags_returning_ids(tags_to_insert, dependencies))
    old_tag_ids = {tag.id for tag in existing_tags}

    return old_tag_ids | new_tag_ids


def insert_task_tags(tag_ids, task_id, dependencies: models.Dependencies):
    tags = list()
    for tag_id in tag_ids:
        tags.append(models.TaskTag(task_id=task_id, tag_id=tag_id))
    save_task_tags(tags, dependencies)


async def task_post(
        request: models.TaskPostRequestBody,
        token: models.Token,
        dependencies: models.Dependencies,
):
    task = convert_to_models_task(request, token.user_id)

    try:
        task_id, task_public_id = save_task_returning_id(task, dependencies)
        if task.tags:
            tag_ids = merge_tags(task.tags, dependencies)
            insert_task_tags(tag_ids, task_id, dependencies)
    except RuntimeError:
        return Response(
            utils.to_json({'message': 'Could not create task'}),
            status_code=400,
        )
    return Response(utils.to_json({'id': task_public_id}), status_code=201)
