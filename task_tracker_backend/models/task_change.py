import datetime as dt
from enum import Enum

from pydantic import BaseModel


class TaskField(Enum):
    NAME = 'name'
    CONTENT = 'content'
    EXECUTOR = 'executor'
    TAGS = 'tags'
    STATUS = 'status'


class TaskChange(BaseModel):
    task_id: str
    field: TaskField
    value_before: str
    value_after: str
    updated_by: str
    updated_at: dt.datetime
