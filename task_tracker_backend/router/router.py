from fastapi import APIRouter
from fastapi import Depends

from task_tracker_backend import auth
from task_tracker_backend import models
from task_tracker_backend import views

api_router = APIRouter(
    prefix='/api',
    tags=['Api'],
    responses={404: {'detail': 'Not found'}},
)


@api_router.get(
    '/task', response_model=models.Task, response_model_exclude_none=True,
)
async def task_get(
        public_id: str, _: models.Token = Depends(auth.validate_token),
):
    """Получение информации о задачи по ее public_id"""
    response = await views.task_get(public_id)
    return response


@api_router.post('/task')
async def task_post(
        body: models.TaskPostRequestBody,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Создание задачи"""
    response = await views.task_post(body, auth_token)
    return response


@api_router.post(
    '/tasks/info',
    response_model=models.TasksInfoPostResponse,
    response_model_exclude_none=True,
)
async def tasks_info_post(
        body: models.TasksInfoPostRequestBody,
        _: models.Token = Depends(auth.validate_token),
):
    """Ручка фильтрации и поиска задач"""
    response = await views.tasks_info_post(body)
    return response


@api_router.post('/task/comment/add', status_code=201)
async def task_comment_add_post(
        public_id: str,
        body: models.CommentAddPostRequestBody,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Ручка добавления комментария к задаче"""
    response = await views.task_comment_add_post(public_id, body, auth_token)
    return response


@api_router.post('/task/status/update')
async def task_status_update_post(
        public_id: str,
        body: models.TaskStatusUpdatePostRequestBody,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Ручка обновления статуса задачи"""
    response = await views.task_status_update_post(
        public_id, body, auth_token
    )
    return response


@api_router.post('/task/timer/start')
async def task_timer_start(
        public_id: str,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Ручка запуска таймера задачи"""
    response = await views.task_timer_start_post(public_id, auth_token)
    return response


@api_router.post('/task/timer/stop')
async def task_timer_stop(
        public_id: str,
        auth_token: models.Token = Depends(auth.validate_token),
):
    """Ручка остановки таймера задачи"""
    response = await views.task_timer_stop_post(public_id, auth_token)
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


@api_router.post(
    '/audit/import-tasks'
)
async def audit_import_tasks(
        _: models.Token = Depends(auth.validate_token)
):
    """Поставить задачу на вышрузку всех задач в xlsx"""
    response = await views.audit_import_tasks_post()
    return response
