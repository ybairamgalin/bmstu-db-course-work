from task_tracker_backend import models

SQL_SAVE_TASK = """
insert into task_tracker.tasks(title, content, creator, executor)
values
    (%s, %s, %s, %s)
returning public_id
"""


def save_task_returning_id(
        task: models.Task, dependencies: models.Dependencies
):
    try:
        db_response = dependencies.pg.execute(
            SQL_SAVE_TASK,
            (task.title, task.content, task.creator_id, task.executor_id),
        )
    except Exception as error:
        raise RuntimeError('Could not create task') from error
    return db_response[0][0]
