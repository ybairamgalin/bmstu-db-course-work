from typing import Optional

import dataclasses
import datetime


@dataclasses.dataclass
class Task(object):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    creator_id: Optional[int] = None
    executor_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
