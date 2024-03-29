from task_tracker_backend import models
from task_tracker_backend import pg


SQL_SELECT_TOKEN_BY_USER_ID = """
select uuid, expires_at, user_id, u.username
from task_tracker.tokens t
left join task_tracker.users u on t.user_id = u.id
where user_id = %s
"""

SQL_SELECT_TOKEN_BY_UUID = """
select uuid, expires_at, user_id, u.username
from task_tracker.tokens t
left join task_tracker.users u on t.user_id = u.id
where uuid = %s
"""


def get_tokens_by_user_id(user_id):
    response = pg.Pg.execute(
        SQL_SELECT_TOKEN_BY_USER_ID, (user_id,),
    )

    tokens = list()
    for row in response:
        tokens.append(
            models.Token(
                uuid=row[0],
                expires_at=row[1],
                user_id=row[2],
                username=row[3],
            ),
        )

    return tokens


def get_token_by_uuid(uuid):
    response = pg.Pg.execute(
        SQL_SELECT_TOKEN_BY_UUID, (uuid,),
    )

    if len(response) == 0:
        return None

    token = response[0]
    return models.Token(
        uuid=token[0],
        expires_at=token[1],
        user_id=token[2],
        username=token[3],
    )
