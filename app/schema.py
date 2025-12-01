from pydantic import BaseModel

import datetime
from typing import Literal

class IdAdvertisement(BaseModel):
    id: int

class SuccessResponse(BaseModel):
    status: Literal['success']

class CreateAdvertisementRequest(BaseModel):
    title: str
    content: str
    price: float
    author: str
    creation_date: datetime.datetime

class CreateAdvertisementResponse(IdAdvertisement):
    pass

class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    price: float | None = None
    author: str | None = None

class UpdateAdvertisementResponse(SuccessResponse):
    pass

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    content: str
    price: float
    author: str
    creation_date: datetime.datetime

class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]

class DeleteAdvertisementResponse(BaseModel):
    pass