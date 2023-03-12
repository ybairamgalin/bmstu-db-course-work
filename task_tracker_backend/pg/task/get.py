import logging

from task_tracker_backend import models

SQL_GET_TASK = """
select id, title, content, creator, executor, created_at, updated_at 
from task_tracker.tasks
where id=%s
"""


def get_task_by_id(task_id: int, dependencies: models.Dependencies):
    try:
        result = dependencies.pg.execute(SQL_GET_TASK, (task_id,))
    except Exception as error:
        logging.log(logging.ERROR, error)
        raise RuntimeError('Could not get task by id') from error
    if len(result) == 0:
        raise RuntimeError(f'No task with id {task_id}')

    db_task = result[0]
    task = models.Task(
        id=db_task[0],
        title=db_task[1],
        content=db_task[2],
        creator_id=db_task[3],
        executor_id=db_task[4],
        created_at=db_task[5],
        updated_at=db_task[6],
    )

    return task
