from task_tracker_backend import pg

from task_tracker_backend.pg.timer.get import get_active_timer

SQL_START_TIMER = """
insert into task_tracker.timers (task_id, started_by)
values (%s, %s);
"""

SQL_STOP_TIMER = """
update task_tracker.timers
set
    stopped_at = now()
where task_id = %s and stopped_at is null
returning stopped_at
"""


def start_task_timer(task_id, user_id):
    started_at, started_by = get_active_timer(task_id)
    if started_at is not None:
        raise RuntimeError('Cannot have more than 1 running timer')

    pg.Pg.execute_no_return(SQL_START_TIMER, (task_id, user_id))


def stop_task_timer(task_id, user_id):
    started_at, started_by = get_active_timer(task_id)
    if started_at is None:
        raise RuntimeError('No active timers found')
    if started_by != user_id:
        raise RuntimeError('Можно остановить только свой таймер')
    stopped_at = pg.Pg.execute(SQL_STOP_TIMER, (task_id,))[0][0]
    return stopped_at - started_at
