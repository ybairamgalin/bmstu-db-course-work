from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.save import save_task_returning_id


def task_from_dict(dict_content):
    task = models.Task()
    if 'author' in dict_content:
        task.creator_id = dict_content['author']
    else:
        raise RuntimeError('No task author specified')
    if 'title' in dict_content:
        task.title = dict_content['title']
    else:
        raise RuntimeError('No task title specified')
    if 'content' in dict_content:
        task.content = dict_content['content']
    if 'executor' in dict_content:
        task.executor_id = dict_content['executor']

    return task


async def task_post(request: dict, dependencies: models.Dependencies):
    if 'task' not in request:
        raise RuntimeError('No task is specified')

    task = task_from_dict(request['task'])
    task_id = save_task_returning_id(task, dependencies)
    return Response(utils.to_json({'id': task_id}), status_code=200)
