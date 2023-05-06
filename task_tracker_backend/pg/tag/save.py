from typing import List

from task_tracker_backend import models

SQL_SAVE_TAGS = """
insert into task_tracker.tags (value)
select unnest(%(tags)s)
on conflict (value) do nothing
returning id
"""


def save_tags_returning_ids(tags: List[str]):
    if not tags:
        return list()
    try:
        return pg.Pg.execute(SQL_SAVE_TAGS, {'tags': tags})
    except Exception as error:
        print(error)
        raise RuntimeError('Could not save tags') from error
