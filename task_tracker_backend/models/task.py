import dataclasses
import datetime as dt

from typing import Optional
from typing import List

from pydantic import BaseModel

from task_tracker_backend.models.user import UserLoginName
from task_tracker_backend.models.task_status import TaskStatus
from task_tracker_backend.models.comment import Comment


class Task(BaseModel):
    public_id: str
    title: str
    creator: UserLoginName
    status: TaskStatus
    created_at: dt.datetime
    updated_at: dt.datetime
    tags: List[str] = list()
    comments: List[Comment] = list()

    content: Optional[str] = None
    topic: Optional[str] = None
    executor: Optional[UserLoginName] = None
    spent_time: Optional[dt.timedelta] = None


@dataclasses.dataclass
class TaskTag:
    task_id: int
    tag_id: int


class TaskStatusUpdatePostRequestBody(BaseModel):
    new_status: TaskStatus


class TaskPostRequestBody(BaseModel):
    title: str
    tags: List[str] = list()
    content: Optional[str] = None
    executor_username: Optional[str] = None


class TasksInfoPostRequestBody(BaseModel):
    limit: int = 10

    tags: List[str] = list()
    name_part: Optional[str] = None
    executor_username: Optional[str] = None
    order_by: Optional[str] = None
    cursor: Optional[bytes] = None


class TasksInfoPostResponse(BaseModel):
    tasks: List[Task]
    cursor: bytes
