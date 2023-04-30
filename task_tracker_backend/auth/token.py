import uuid
import datetime as dt

from task_tracker_backend import models

from task_tracker_backend.pg.token.get import get_tokens_by_user_id
from task_tracker_backend.pg.token.save import save_token_returning_uuid

TOKEN_LIFETIME = dt.timedelta(hours=1)
TOKEN_RENEW_TIME = dt.timedelta(minutes=10)


def make_new_token(user_id):
    return models.Token(
        uuid=str(uuid.uuid4()),
        expires_at=dt.datetime.now() + TOKEN_LIFETIME,
        user_id=user_id,
    )


def get_user_token(user_id, dependencies: models.Dependencies):
    """Возвращает существующий или создает новый токен"""
    tokens = get_tokens_by_user_id(user_id, dependencies)
    if len(tokens) == 0:
        token = make_new_token(user_id)
        return save_token_returning_uuid(token, dependencies)

    tokens.sort(key=lambda t: t.expires_at, reverse=True)
    latest_token = tokens[0]
    if dt.datetime.now() + TOKEN_RENEW_TIME > latest_token.expires_at:
        token = make_new_token(user_id)
        return save_token_returning_uuid(token, dependencies)

    return latest_token.uuid


# def validate_user(x_user_token: str, dependencies: models.Dependencies):
#     unauthorized_response = Response(
#         utils.to_json({'message': 'Unauthorized'}),
#         status_code=401
#     )
#     if x_user_token is None:
#         return unauthorized_response
#     token = get_token_by_uuid(x_user_token, dependencies)
#     if token is None:
#         return unauthorized_response
#
#     if token.expires_at < dt.datetime.utcnow():
#         return unauthorized_response
#
#     return Response(
#         status_code=200,
#         headers={constants.X_USER_TOKEN_HEADER: x_user_token}
#     )

