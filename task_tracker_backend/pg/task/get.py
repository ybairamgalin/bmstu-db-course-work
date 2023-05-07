import logging
import datetime as dt

from task_tracker_backend import models
from task_tracker_backend import pg

from task_tracker_backend.pg.tag.get import get_tags_by_task_id

SQL_GET_TASK = """
select id, title, content, creator, executor, created_at, updated_at 
from task_tracker.tasks
where id = %s
"""

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
    status
from task_tracker.tasks t
left join task_tracker.users creator on t.creator = creator.id
left join task_tracker.users executor on t.executor = executor.id
where t.public_id = %s;
"""

SQL_GET_TASKS = """
select t.title, u1.name, u2.name, t.created_at, t.updated_at, t.public_id
from task_tracker.tasks t
    left join task_tracker.users u1 on t.creator = u1.id
    left join task_tracker.users u2 on t.executor = u2.id
where created_at < %s
  and lower(t.title) like %s
order by created_at desc 
limit %s
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
        title=db_task[1],
        created_at=db_task[3],
        updated_at=db_task[4],
        creator=models.UserLoginName(login=db_task[5], name=db_task[6]),
        tags=get_tags_by_task_id(task_id),
        status=models.TaskStatus.map_db_status(db_task[9])
    )
    if db_task[2]:
        result.content = db_task[2]
    if db_task[7] and db_task[8]:
        result.executor = models.UserLoginName(
            login=db_task[7], name=db_task[8]
        )

    return result


def get_tasks(
        name_part: str, last_created_at: dt.datetime, limit: int,
):
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
        tasks.append({
            'title': row[0],
            'creator': row[1],
            'executor': row[2],
            'created_at': row[3],
            'updated_at': row[4],
            'public_id': row[5],
        })

    return tasks
