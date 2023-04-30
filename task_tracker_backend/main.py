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


@task_tracker.get('/api/task')
async def task_get(task_id: int):
    response = await views.task_get(task_id, dependencies)
    return response


@task_tracker.post('/api/task')
async def task_post(
        body: models.TaskPostRequestBody,
        x_user_id: Union[str, None] = Header(default=None),
):
    response = await views.task_post(body, x_user_id, dependencies)
    return response


@task_tracker.post('/api/task/info')
async def task_info_post(body: models.TaskInfoPostRequestBody):
    response = await views.task_info_post(body, dependencies)
    return response


@task_tracker.get('/api/topic/info')
async def topic_info_get():
    response = await views.topic_info_get(dependencies)
    return response


@task_tracker.post('/api/user/create')
async def user_create_post(body: models.UserCreatePostRequest):
    """Регистрация нового пользователя"""
    response = await views.user_create_post(body, dependencies)
    return response
