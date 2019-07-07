import enum
from typing import Optional

import pydantic
from aiohttp import web
from pydantic import BaseModel

routes = web.RouteTableDef()


class SubmitRequest(BaseModel):
    url: pydantic.UrlStr
    email: Optional[pydantic.EmailStr] = ""


class TaskStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    DONE = "DONE"
    FAILED = "FAILED"


class TaskState(BaseModel):
    url: pydantic.UrlStr
    email: Optional[pydantic.EmailStr]
    status: TaskStatus
    md5: str = ""  # calculated md5 value
    err: Optional[str] = ""  # error message in case of failure


class CheckRequest(BaseModel):
    id: str
