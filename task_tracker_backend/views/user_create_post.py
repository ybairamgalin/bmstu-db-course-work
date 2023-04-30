from starlette.responses import Response

from task_tracker_backend import models
from task_tracker_backend import auth
from task_tracker_backend import utils
from task_tracker_backend import constants

from task_tracker_backend.pg.user.get import user_in_database
from task_tracker_backend.pg.user.save import save_user_returning_id


async def user_create_post(
        request: models.UserCreatePostRequest,
        dependencies: models.Dependencies
):
    if user_in_database(request.username, dependencies):
        return Response(
            utils.to_json(
                {'message': f'User with name {request.username} already exists'}
            ),
            status_code=409,
        )

    new_db_user = auth.map_request_user_to_db_user(request)
    user_id = save_user_returning_id(new_db_user, dependencies)
    token = auth.get_user_token(user_id, dependencies)

    return Response(
        utils.to_json({'username': request.username}),
        headers={constants.X_USER_TOKEN_HEADER: token},
        status_code=201,
    )
