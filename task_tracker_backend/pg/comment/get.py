from task_tracker_backend import models

from task_tracker_backend import pg

SQL_SELECT_COMMENTS = """
select c.text, c.created_at, u.name, u.username
from task_tracker.comments c
left join task_tracker.users u on u.id = c.author_id
where task_id = %s
"""


def get_comments_by_task_id(task_id: int):
    result = pg.Pg.execute(SQL_SELECT_COMMENTS, (task_id,))
    if len(result) == 0:
        return list()
    return [
        models.Comment(
            text=row[0],
            created_at=row[1],
            author=models.UserLoginName(
                name=row[2],
                login=row[3],
            ),
        ) for row in result
    ]
