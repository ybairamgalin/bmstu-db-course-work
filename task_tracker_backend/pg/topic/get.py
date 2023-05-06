from task_tracker_backend import pg

SQL_GET_ALL_TOPIC_NAMES = """
select id, name from task_tracker.topics
"""


def get_all_topic_names():
    result = pg.Pg.execute(SQL_GET_ALL_TOPIC_NAMES)
    return [{'id': row[0], 'name': row[1]} for row in result]
