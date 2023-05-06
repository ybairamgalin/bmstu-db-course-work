from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from task_tracker_backend import models
from task_tracker_backend import pg
from task_tracker_backend import router

task_tracker = FastAPI()

models.Config.load_config()
pg.Pg.open_connection(models.Config.get_item('postgres'))

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

task_tracker.include_router(router.api_router)
