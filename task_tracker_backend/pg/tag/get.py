from task_tracker_backend import models

SQL_GET_TAGS = """
select id,value
from task_tracker.tags
where value in (select unnest(%(tags)s))
"""


def get_tags_by_values(tags, dependencies: models.Dependencies):
    result = dependencies.pg.execute(SQL_GET_TAGS, {'tags': tags})

    tags = list()
    for row in result:
        tags.append(models.Tag(id=row[0], value=row[1]))

    return tags
