from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    LOG = 0
    ALARM = 1


class Message(BaseModel):
    status: Status
    head: str
    body: str
    dashboard: str
