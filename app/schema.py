from pydantic import BaseModel

import datetime
from typing import Literal

class IdAnnouncement(BaseModel):
    id: int

class SuccessResponse(BaseModel):
    status: Literal['success']

class CreateAnnouncementRequest(BaseModel):
    title: str
    content: str
    price: float
    autor: str
    creation_date: datetime.datetime

class CreateAnnouncementResponse(IdAnnouncement):
    pass

class UpdateAnnouncementRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    price: float | None = None
    autor: str | None = None

class UpdateAnnouncementResponse(SuccessResponse):
    pass

class GetAnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    price: float
    autor: str
    creation_date: datetime.datetime

class SearchAnnouncementResponse(BaseModel):
    results: list[GetAnnouncementResponse]

class DeleteAnnouncementResponse(BaseModel):
    pass