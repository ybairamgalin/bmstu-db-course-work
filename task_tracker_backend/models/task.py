import dataclasses
import datetime as dt

from enum import Enum

from typing import Union
from typing import Optional
from typing import List

from pydantic import BaseModel

from task_tracker_backend.models.user import UserLoginName


class TaskStatus(str, Enum):
    open = 'Открыт'
    in_progress = 'В работе'
    blocked = 'Требуется информация'
    in_review = 'На ревью'
    closed = 'Закрыт'

    @staticmethod
    def map_db_status(db_status: str):
        if db_status == 'open':
            return TaskStatus.open
        if db_status == 'in_progress':
            return TaskStatus.in_progress
        if db_status == 'in_review':
            return TaskStatus.in_review
        if db_status == 'information_required':
            return TaskStatus.blocked
        if db_status == 'closed':
            return TaskStatus.closed

        raise RuntimeError('Map db status ')


class Task(BaseModel):
    title: str
    creator: UserLoginName
    tags: List[str]
    status: TaskStatus
    created_at: dt.datetime
    updated_at: dt.datetime

    content: Optional[str]
    topic: Optional[str]
    executor: Optional[UserLoginName]


@dataclasses.dataclass
class TaskTag:
    task_id: int
    tag_id: int


class TaskPostRequestBody(BaseModel):
    title: str
    tags: List[str] = None
    content: Union[str, None] = None
    executor_username: Union[str, None] = None


class TaskInfoPostRequestBody(BaseModel):
    cursor: Union[str, None] = None
    name_part: Union[str, None] = None
    topic: Union[str, None] = None
    order_by: Union[str, None] = None
    executor_username: Union[str, None] = None
