import dataclasses

from typing import List

from pydantic import BaseModel


class UserLoginName(BaseModel):
    name: str
    login: str


class UserCreatePostRequest(BaseModel):
    username: str
    name: str
    hashed_password: str


class UserCreatePostResponse(BaseModel):
    username: str


class UserAuthPostRequest(BaseModel):
    username: str
    hashed_password: str


class UsersFindGetResponse(BaseModel):
    users: List[UserLoginName]


@dataclasses.dataclass
class DbUser:
    username: str
    name: str
    salted_password: str
    salt: str
