from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import utils

from task_tracker_backend.pg.user.get import get_users_by_name_part


MAX_LIMIT = 100


async def users_find_get(
        query: str, user_limit, dependencies: models.Dependencies,
):
    limit = min(MAX_LIMIT, user_limit)
    users = get_users_by_name_part(query, limit, dependencies)
    response_json = {'users': list()}
    for user in users:
        response_json['users'].append(
            {
                'name': user.name,
                'login': user.login,
            }
        )

    return Response(utils.to_json(response_json), 200)
