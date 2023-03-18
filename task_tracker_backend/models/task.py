import dataclasses
import datetime

from typing import Optional
from typing import Union

from pydantic import BaseModel


@dataclasses.dataclass
class Task:
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    creator_id: Optional[int] = None
    executor_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class TaskPostRequestBody(BaseModel):
    title: str
    content: Union[str, None] = None
