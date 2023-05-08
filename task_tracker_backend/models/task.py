import dataclasses
import datetime as dt

from enum import Enum

from typing import Union
from typing import Optional
from typing import List

from pydantic import BaseModel

from task_tracker_backend.models.user import UserLoginName
from task_tracker_backend.models.task_status import TaskStatus
from task_tracker_backend.models.comment import Comment


class Task(BaseModel):
    title: str
    creator: UserLoginName
    tags: List[str]
    comments: List[Comment]
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


class TaskStatusUpdatePostRequestBody(BaseModel):
    new_status: TaskStatus


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
