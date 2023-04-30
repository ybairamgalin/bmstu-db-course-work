from task_tracker_backend import models

SQL_SELECT_USER_ID_BY_USERNAME = """
select id
from task_tracker.users
where username = %s
"""

SQL_SELECT_USER_BY_USERNAME = """
select id, username, name, password, salt
from task_tracker.users
where username = %s
"""


def user_in_database(username, dependencies: models.Dependencies):
    response = (
        dependencies.pg.execute(SQL_SELECT_USER_ID_BY_USERNAME, (username,))
    )
    return len(response) > 0


def get_user_by_username(username, dependencies: models.Dependencies):
    response = dependencies.pg.execute(
        SQL_SELECT_USER_BY_USERNAME, (username,),
    )
    if len(response) == 0:
        return None, None

    db_user = response[0]
    user_id = db_user[0]
    return user_id, models.DbUser(
        username=db_user[1],
        name=db_user[2],
        salted_password=db_user[3],
        salt=db_user[4],
    )
