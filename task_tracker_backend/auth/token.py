import uuid
import datetime as dt

from fastapi import HTTPException

from task_tracker_backend import constants
from task_tracker_backend import models

from task_tracker_backend.pg.token.get import get_tokens_by_user_id
from task_tracker_backend.pg.token.get import get_token_by_uuid
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


def validate_token(x_user_token: str, dependencies: models.Dependencies):
    if x_user_token is None:
        raise HTTPException(401, f'Missing {constants.X_USER_TOKEN_HEADER} header')
    token = get_token_by_uuid(x_user_token, dependencies)
    if token is None:
        raise HTTPException(401, f'Bad token')

    if token.expires_at < dt.datetime.utcnow():
        raise HTTPException(401, f'Token has expired')

    return token
