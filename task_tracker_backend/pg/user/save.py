from task_tracker_backend import models
from task_tracker_backend import pg

SQL_SAVE_USER = """
insert into task_tracker.users(username, name, salt, password)
values (%s, %s, %s, %s)
returning id
"""


def save_user_returning_id(user: models.DbUser):
    try:
        db_response = pg.Pg.execute(
            SQL_SAVE_USER,
            (user.username, user.name, user.salt, user.salted_password),
        )
    except Exception as error:
        raise RuntimeError('Could not create user') from error
    return db_response[0][0]
