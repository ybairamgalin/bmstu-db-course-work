from typing import List

from task_tracker_backend import models
from task_tracker_backend import pg

from task_tracker_backend.pg.user.get import get_user_by_username

SQL_SAVE_TASK = """
insert into task_tracker.tasks(title, content, creator, executor)
values
    (%s, %s, %s, %s)
returning id, public_id
"""

SQL_SAVE_TASK_TAGS = """
insert into task_tracker.task_tags(task_id, tag_id)
select task_id, tag_id 
from unnest(%(task_tags)s::task_tracker.task_tag_v1[])
on conflict (task_id, tag_id) do nothing
"""


def save_task_returning_id(task: models.TaskPostRequestBody, user_id):
    try:
        executor_id = None
        if task.executor_username:
            executor_id, _ = get_user_by_username(task.executor_username)
        db_response = pg.Pg.execute(
            SQL_SAVE_TASK,
            (task.title, task.content, user_id, executor_id),
        )
    except Exception as error:
        raise RuntimeError('Could not create task') from error
    return db_response[0]


def save_task_tags(task_tags: List[models.TaskTag]):
    pg.Pg.execute_no_return(
        SQL_SAVE_TASK_TAGS,
        args={
            'task_tags': [
                (task_tag.task_id, task_tag.tag_id) for task_tag in task_tags
            ]
        }
    )
