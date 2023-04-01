from task_tracker_backend import models

SQL_GET_ALL_TOPIC_NAMES = """
select name from task_tracker.topics
"""


def get_all_topic_names(dependencies: models.Dependencies):
    result = dependencies.pg.execute(SQL_GET_ALL_TOPIC_NAMES)
    return [row[0] for row in result]
