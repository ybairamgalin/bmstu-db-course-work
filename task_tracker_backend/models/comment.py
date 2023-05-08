import datetime as dt

from pydantic import BaseModel

from task_tracker_backend.models.user import UserLoginName


class CommentAddPostRequestBody(BaseModel):
    text: str


class Comment(BaseModel):
    text: str
    author: UserLoginName
    created_at: dt.datetime
