from typing import List

import logging
import datetime as dt
import uuid

from task_tracker_backend import models
from task_tracker_backend import pg
from task_tracker_backend import utils

from task_tracker_backend.pg.tag.get import get_tags_by_task_id
from task_tracker_backend.pg.comment.get import get_comments_by_task_id

SQL_GET_TASK_BY_PUBLIC_ID = """
select 
    t.id,
    t.title,
    content,
    created_at,
    updated_at,
    creator.username,
    creator.name,
    executor.username,
    executor.name,
    status,
    spent_time,
    t.public_id
from task_tracker.tasks t
left join task_tracker.users creator on t.creator = creator.id
left join task_tracker.users executor on t.executor = executor.id
where t.public_id = %s;
"""

SQL_GET_TASKS = """
select 
    t.title,
    u1.name,
    u1.username,
    u2.name,
    u2.username,
    t.status,
    t.created_at,
    t.updated_at,
    t.public_id,
    t.id
from task_tracker.tasks t
    left join task_tracker.users u1 on t.creator = u1.id
    left join task_tracker.users u2 on t.executor = u2.id
where created_at < %s
  and lower(t.title) like %s
order by created_at desc
limit %s
"""

SQL_GET_TASK_ID_BY_PUBLIC_ID = """
select id
from task_tracker.tasks
where public_id = %s
"""


def get_task_by_public_id(public_id: str):
    db_tasks = pg.Pg.execute(SQL_GET_TASK_BY_PUBLIC_ID, (public_id,))
    if not db_tasks:
        logging.info('Task with public_id %s was not found', public_id)
        raise RuntimeError('Task now found')
    if len(db_tasks) > 1:
        logging.error('Duplicate tasks with public id %s', public_id)
        raise RuntimeError('Duplicate tasks')

    db_task = db_tasks[0]
    task_id = db_task[0]
    result = models.Task(
        public_id=db_task[11],
        title=db_task[1],
        created_at=db_task[3],
        updated_at=db_task[4],
        creator=models.UserLoginName(login=db_task[5], name=db_task[6]),
        tags=get_tags_by_task_id(task_id),
        comments=sorted(
            get_comments_by_task_id(task_id), key=lambda x: x.created_at,
        ),
        status=models.TaskStatus.map_db_status(db_task[9])
    )
    if db_task[2]:
        result.content = db_task[2]
    if db_task[7] and db_task[8]:
        result.executor = models.UserLoginName(
            login=db_task[7], name=db_task[8]
        )
    if db_task[10]:
        result.spent_time = db_task[10]

    return result


def get_task_id_by_public_id(public_id: str):
    if not utils.is_valid_uuid(public_id):
        raise RuntimeError(f'Public id {public_id} is not a valid uuid')

    result = pg.Pg.execute(SQL_GET_TASK_ID_BY_PUBLIC_ID, (public_id,))
    if len(result) != 1:
        raise RuntimeError(f'No task with public id {public_id}')

    return result[0][0]


def get_tasks(
        name_part: str,
        last_created_at: dt.datetime,
        limit: int = 1000,
) -> List[models.Task]:
    try:
        result = pg.Pg.execute(
            SQL_GET_TASKS,
            (
                last_created_at,
                f'%{name_part.lower()}%' if name_part else '%',
                limit,
            )
        )

    except Exception as error:
        logging.log(logging.ERROR, error)
        raise RuntimeError('Could not get tests') from error

    tasks = list()
    for row in result:
        tasks.append(
            models.Task(
                public_id=row[8],
                title=row[0],
                creator=models.UserLoginName(
                    name=row[1],
                    login=row[2],
                ),
                executor=models.UserLoginName(
                    name=row[3],
                    login=row[4],
                )
                if row[3] else None,

                status=models.TaskStatus.map_db_status(row[5]),
                created_at=row[6],
                updated_at=row[7],
                tags=get_tags_by_task_id(row[9])
            )
        )

    return tasks
