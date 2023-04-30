from task_tracker_backend import models

SQL_INSERT_TOKEN = """
insert into task_tracker.tokens(uuid, user_id, expires_at)
values (%s, %s, %s)
returning uuid
"""

def save_token_returning_uuid(
        token: models.Token, dependencies: models.Dependencies
):
    response = dependencies.pg.execute(
        SQL_INSERT_TOKEN, (token.uuid, token.user_id, token.expires_at)
    )
    return response[0][0]
