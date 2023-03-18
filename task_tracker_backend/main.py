from typing import Union

from fastapi import FastAPI, Header

from task_tracker_backend import models
from task_tracker_backend import views

print(__name__)
task_tracker = FastAPI()
dependencies = models.Dependencies()
print('Starting web server backend')


@task_tracker.get('/task')
async def task_get(task_id: int):
    response = await views.task_get(task_id, dependencies)
    return response


@task_tracker.post('/task')
async def task_post(
        body: models.TaskPostRequestBody,
        x_user_id: Union[str, None] = Header(default=None),
):
    response = await views.task_post(body, x_user_id, dependencies)
    return response
