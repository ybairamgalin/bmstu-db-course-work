import datetime as dt

from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.task.get import get_tasks


async def tasks_info_post(request: models.TasksInfoPostRequestBody):
    db_tasks = get_tasks(
        request.name_part,
        dt.datetime.fromisoformat(request.cursor.decode('utf-8'))
        if request.cursor else dt.datetime.now(),
    )

    tags = set(request.tags)
    filtered_tasks = list()
    for task in db_tasks:
        if request.executor_username:
            if not task.executor:
                continue
            if task.executor.login != request.executor_username:
                continue
        if tags:
            if not tags.issubset(task.tags):
                continue
        filtered_tasks.append(task)
        if len(filtered_tasks) >= request.limit:
            break

    return models.TasksInfoPostResponse(
        tasks=filtered_tasks,
        cursor=(
            filtered_tasks[-1].created_at.isoformat().encode()
            if len(filtered_tasks) else dt.datetime.now().isoformat().encode()
        )
    )
