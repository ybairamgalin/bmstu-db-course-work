from starlette.responses import Response

from task_tracker_backend import auth
from task_tracker_backend import utils
from task_tracker_backend import models
from task_tracker_backend import constants

from task_tracker_backend.pg.user.get import get_user_by_username


async def user_auth_post(auth_request: models.UserAuthPostRequest):
    unauthorized_response = Response(
        utils.to_json({'message': 'Unauthorized'}),
        status_code=401
    )

    user_id, db_user = get_user_by_username(auth_request.username)
    if db_user is None:
        return unauthorized_response
    user_salted_password = auth.hash_password_with_salt(
        auth_request.hashed_password, db_user.salt
    )
    # TODO make safe comparison
    if user_salted_password != db_user.salted_password:
        return unauthorized_response

    token = auth.get_user_token(user_id)
    return Response(
        utils.to_json({
            constants.X_USER_TOKEN_HEADER: token,
            'name': db_user.name,
        }),
        status_code=200,
    )
