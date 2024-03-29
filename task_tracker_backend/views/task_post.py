from typing import List

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils

from task_tracker_backend.pg.task.save import save_task_returning_id
from task_tracker_backend.pg.task.save import save_task_tags
from task_tracker_backend.pg.tag.save import save_tags_returning_ids
from task_tracker_backend.pg.tag.get import get_tags_by_values


def trim_tags(tags: List[str]):
    return [tag.strip() for tag in tags]


def get_tags_to_insert(new_tags: List[str], existing_tags: set[str]):
    tags_to_insert = list()
    for tag in new_tags:
        if tag in existing_tags:
            continue

        tags_to_insert.append(tag)

    return tags_to_insert


def merge_tags(tags):
    existing_tags = get_tags_by_values(tags)

    existing_tags_values = {tag.value for tag in existing_tags}
    tags_to_insert = get_tags_to_insert(tags, existing_tags_values)

    new_tag_ids = set(save_tags_returning_ids(tags_to_insert))
    old_tag_ids = {tag.id for tag in existing_tags}

    return old_tag_ids | new_tag_ids


def insert_task_tags(tag_ids, task_id):
    tags = list()
    for tag_id in tag_ids:
        tags.append(models.TaskTag(task_id=task_id, tag_id=tag_id))
    save_task_tags(tags)


async def task_post(request: models.TaskPostRequestBody, token: models.Token):
    try:
        task_id, task_public_id = save_task_returning_id(request, token.user_id)
        if request.tags:
            tag_ids = merge_tags(request.tags)
            insert_task_tags(tag_ids, task_id)
    except RuntimeError:
        return Response(
            utils.to_json({'message': 'Could not create task'}),
            status_code=400,
        )
    return Response(utils.to_json({'id': task_public_id}), status_code=201)
