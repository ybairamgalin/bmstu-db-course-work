import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

from task_tracker_backend import models
from task_tracker_backend import pg
from task_tracker_backend import kafka
from task_tracker_backend import clickhouse
from task_tracker_backend import utils
from task_tracker_backend import router

task_tracker = FastAPI()

models.Config.load_config()
pg.Pg.open_connection(models.Config.get_item('postgres'))
kafka.Producer.open_connection(models.Config.get_item('kafka-producer'))
clickhouse.Clickhouse.open_connection(models.Config.get_item('clickhouse'))
utils.setup_logging()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:80",
]
task_tracker.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_tracker.include_router(router.api_router)


@task_tracker.get('/ping')
async def ping_get():
    """Ручка проверки, что сервис работает"""
    return Response(status_code=200)


@task_tracker.exception_handler(500)
async def exception_handler(request: Request, exc: Exception):
    """Логирование ошибок 500"""
    logging.error(
        'method=%s status_code=500 exception=%s', request.method, exc
    )
    return utils.to_json({'code': 500, 'message': 'Internal server error'})
