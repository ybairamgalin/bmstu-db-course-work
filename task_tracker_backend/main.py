from typing import Union

from fastapi import FastAPI
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware

from task_tracker_backend import auth
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
    """Получение информации о задачи по ее id"""
    response = await views.task_get(task_id, dependencies)
    return response


@task_tracker.post('/api/task')
async def task_post(
        body: models.TaskPostRequestBody,
        x_user_token: Union[str, None] = Header(default=None),
):
    """Создание задачи"""
    auth_token = auth.validate_token(x_user_token, dependencies)
    response = await views.task_post(body, auth_token, dependencies)
    return response


@task_tracker.post('/api/task/info')
async def task_info_post(
        body: models.TaskInfoPostRequestBody,
        x_user_token: Union[str, None] = Header(default=None),
):
    auth.validate_token(x_user_token, dependencies)
    response = await views.task_info_post(body, dependencies)
    return response


@task_tracker.get('/api/topic/info')
async def topic_info_get(
        x_user_token: Union[str, None] = Header(default=None),
):
    """Получение информации о топиках"""
    auth.validate_token(x_user_token, dependencies)
    response = await views.topic_info_get(dependencies)
    return response


@task_tracker.post(
    '/api/user/create',
    status_code=201,
    response_model=models.UserCreatePostResponse,
    responses={409: {"model": models.ErrorResponse}},
)
async def user_create_post(body: models.UserCreatePostRequest):
    """Регистрация нового пользователя"""
    response = await views.user_create_post(body, dependencies)
    return response


@task_tracker.post('/api/user/auth')
async def user_auth_post(body: models.UserAuthPostRequest):
    """Авторизация пользователя"""
    response = await views.user_auth_post(body, dependencies)
    return response
