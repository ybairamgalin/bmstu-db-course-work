import logging
import datetime as dt

from task_tracker_backend import models
from task_tracker_backend import pg

SQL_GET_TASK = """
select id, title, content, creator, executor, created_at, updated_at 
from task_tracker.tasks
where id = %s
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


def map_db_task_to_models_task(db_task):
    return models.Task(
        id=db_task[0],
        title=db_task[1],
        content=db_task[2],
        creator_id=db_task[3],
        executor_id=db_task[4],
        created_at=db_task[5],
        updated_at=db_task[6],
    )


def get_task_by_id(task_id: int):
    try:
        result = pg.Pg.execute(SQL_GET_TASK, (task_id,))
    except Exception as error:
        logging.log(logging.ERROR, error)
        raise RuntimeError('Could not get task by id') from error
    if len(result) == 0:
        raise RuntimeError(f'No task with id {task_id}')

    db_task = result[0]
    task = map_db_task_to_models_task(db_task)
    return task


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
