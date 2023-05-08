from task_tracker_backend import pg

SQL_SAVE_COMMENT = """
insert into task_tracker.comments (text, task_id, author_id)
values 
    (%s, %s, %s)
"""


def save_comment(text, task_id, author_id):
    pg.Pg.execute_no_return(SQL_SAVE_COMMENT, (text, task_id, author_id))
