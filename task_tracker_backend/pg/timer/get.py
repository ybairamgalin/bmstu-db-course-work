from task_tracker_backend import pg

SQL_GET_ACTIVE_TIMER = """
select started_at, started_by
from task_tracker.timers
where task_id = %s and stopped_at is null;
"""


def get_active_timer(task_id):
    result = pg.Pg.execute(SQL_GET_ACTIVE_TIMER, (task_id, ))
    if len(result) != 1:
        return None, None
    return result[0][0], result[0][1]
