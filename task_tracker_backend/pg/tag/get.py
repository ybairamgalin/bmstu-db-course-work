from task_tracker_backend import models
from task_tracker_backend import pg

SQL_GET_TAGS = """
select id,value
from task_tracker.tags
where value in (select unnest(%(tags)s))
"""

SQL_GET_TAGS_BY_TASK_ID = """
select value
from task_tracker.task_tags tt
left join task_tracker.tags t on tt.tag_id = t.id
where tt.task_id = %s
"""


def get_tags_by_values(tags):
    result = pg.Pg.execute(SQL_GET_TAGS, {'tags': tags})

    tags = list()
    for row in result:
        tags.append(models.Tag(id=row[0], value=row[1]))

    return tags


def get_tags_by_task_id(task_id: int):
    db_tags = pg.Pg.execute(SQL_GET_TAGS_BY_TASK_ID, (task_id,))
    return [row[0] for row in db_tags]
