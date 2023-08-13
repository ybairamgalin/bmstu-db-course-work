import dataclasses
import datetime

from typing import Optional


@dataclasses.dataclass
class Token:
    uuid: str
    expires_at: datetime.datetime
    user_id: int
    username: Optional[str] = None
