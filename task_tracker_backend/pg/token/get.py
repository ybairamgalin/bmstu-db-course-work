from task_tracker_backend import models


SQL_SELECT_TOKEN_BY_USER_ID = """
select uuid, expires_at, user_id
from task_tracker.tokens
where user_id = %s
"""


def get_tokens_by_user_id(user_id, dependencies: models.Dependencies):
    response = dependencies.pg.execute(
        SQL_SELECT_TOKEN_BY_USER_ID, (user_id,),
    )

    tokens = list()
    for row in response:
        tokens.append(
            models.Token(uuid=row[0], expires_at=row[1], user_id=row[2]),
        )

    return tokens
