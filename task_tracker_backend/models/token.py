import dataclasses
import datetime


@dataclasses.dataclass
class Token:
    uuid: str
    expires_at: datetime.datetime
    user_id: int
