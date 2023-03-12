import json

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import views
from task_tracker_backend import utils

print(__name__)
task_tracker = FastAPI()
dependencies = models.Dependencies()
print('Starting web server backend')


def _get_dict_from_body(body):
    return json.loads(body.decode())


async def _try_handle_request(body, handler):
    try:
        response = await handler(body, dependencies)
        return response
    except RuntimeError as e:
        return Response(utils.to_json({'message': str(e)}), status_code=400)


# @task_tracker.post('/task')
# async def task_post(*, request: Request):
#     body = await request.body()
#     response = await _try_handle_request(
#         _get_dict_from_body(body), views.task_get
#     )
#     return response


@task_tracker.get('/task')
async def task_get(task_id: int):
    response = await views.task_get(task_id, dependencies)
    return response
