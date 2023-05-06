import dataclasses
import datetime

from typing import Optional
from typing import Union
from typing import List

from pydantic import BaseModel

from task_tracker_backend.models.user import UserLoginName


@dataclasses.dataclass
class Task:
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    tags: List[str] = None
    creator_id: Optional[int] = None
    executor_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


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
