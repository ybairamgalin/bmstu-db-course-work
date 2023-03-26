from typing import Union

from fastapi import FastAPI
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware

from task_tracker_backend import models
from task_tracker_backend import views

print(__name__)
task_tracker = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
]
task_tracker.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
