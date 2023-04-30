import dataclasses

from pydantic import BaseModel


class UserCreatePostRequest(BaseModel):
    username: str
    name: str
    hashed_password: str


@dataclasses.dataclass
class DbUser:
    username: str
    name: str
    salted_password: str
    salt: str
