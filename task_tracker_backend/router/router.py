from fastapi import APIRouter
from fastapi import Depends

from task_tracker_backend import auth
from task_tracker_backend import models
from task_tracker_backend import views

api_router = APIRouter(
    prefix='/api',
    tags=['API'],
    responses={404: {'detail': 'Not found'}}
)


@api_router.get('/task')
async def task_get(
        task_id: int, _: models.Token = Depends(auth.validate_token),
):
    """Получение информации о задачи по ее id"""
    response = await views.task_get(task_id)
    return response


@api_router.post('/task')
async def task_post(
        body: models.TaskPostRequestBody,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Создание задачи"""
    response = await views.task_post(body, auth_token)
    return response


@api_router.post('/task/info')
async def task_info_post(
        body: models.TaskInfoPostRequestBody,
        _: models.Token = Depends(auth.validate_token),
):
    """Ручка фильтрации и поиска задач"""
    response = await views.task_info_post(body)
    return response


@api_router.get('/topic/info')
async def topic_info_get(_: models.Token = Depends(auth.validate_token)):
    """Получение информации о всех топиках"""
    response = await views.topic_info_get()
    return response


@api_router.post(
    '/user/create',
    status_code=201,
    response_model=models.UserCreatePostResponse,
    responses={409: {"model": models.ErrorResponse}},
)
async def user_create_post(body: models.UserCreatePostRequest):
    """Регистрация нового пользователя"""
    response = await views.user_create_post(body)
    return response


@api_router.post('/user/auth')
async def user_auth_post(body: models.UserAuthPostRequest):
    """Авторизация пользователя"""
    response = await views.user_auth_post(body)
    return response


@api_router.get(
    '/users/find', response_model=models.UsersFindGetResponse,
)
async def users_find_get(
        query: str,
        limit: int = 7,
        _: models.Token = Depends(auth.validate_token),
):
    """Поиск пользователя по части имени или логина"""
    response = await views.users_find_get(query, limit)
    return response
