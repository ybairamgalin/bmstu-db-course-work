from task_tracker_backend import models

SQL_SELECT_USER_ID_BY_USERNAME = """
select id
from task_tracker.users
where username = %s
"""


def user_in_database(username, dependencies: models.Dependencies):
    response = (
        dependencies.pg.execute(SQL_SELECT_USER_ID_BY_USERNAME, (username,))
    )
    return len(response) > 0
