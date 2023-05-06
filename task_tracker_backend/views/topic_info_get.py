from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils
from task_tracker_backend.pg.topic.get import get_all_topic_names


async def topic_info_get():
    topics = get_all_topic_names()
    response_dict = {
        'topics': topics
    }
    return Response(utils.to_json(response_dict), status_code=200)
