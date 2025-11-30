from fastapi import FastAPI
from sqlalchemy import select

import datetime
from schema import (CreateAnnouncementRequest, CreateAnnouncementResponse, DeleteAnnouncementResponse,
                    GetAnnouncementResponse, SearchAnnouncementResponse, UpdateAnnouncementRequest,
                    UpdateAnnouncementResponse)
from lifespan import Lifespan
from dependency import SessionDependency
import CRUD
import models
from constant import SUCCESS_RESPONSE
from models import Session

app = FastAPI(
    title='Avito',
    description='otivA',
    lifespan=Lifespan
)

@app.post('/announcements', response_model=CreateAnnouncementResponse)
async def create_announcement(announcement: CreateAnnouncementRequest, session: SessionDependency):
    announcement_dict = announcement.model_dump(exclude_unset=True, exclude={"creation_date"})
    announcement_orm_obj = models.Announcement(**announcement_dict)
    await CRUD.add_item(session, announcement_orm_obj)
    return announcement_orm_obj.id_dict


@app.get('/announcements/{announcement_id}', response_model=GetAnnouncementResponse)
async def get_announcements(announcement_id: int, session: SessionDependency):
    announcement_orm_obj = await CRUD.get_item_by_id(session, models.Announcement, announcement_id)
    return announcement_orm_obj.dict

@app.get('/announcements/', response_model=SearchAnnouncementResponse)
async def search_announcements(session: SessionDependency,
                               title: str | None = None,
                               content: str | None = None,
                               price: float | None = None,
                               autor: str | None = None):
    filters = []
    if title is not None:
        filters.append(models.Announcement.title == title)
    if content is not None:
        filters.append(models.Announcement.content == content)
    if price is not None:
        filters.append(models.Announcement.price == price)
    if autor is not None:
        filters.append(models.Announcement.autor == autor)

    query = select(models.Announcement)
    if filters:
        query = query.where(*filters)
    query = query.limit(10000)

    announcements = await session.scalars(query)
    return {'results': [announcement.dict for announcement in announcements]}

@app.patch('/announcements/{announcement_id}', response_model=UpdateAnnouncementResponse)
async def update_announcements(announcement_id: int, announcement_data: UpdateAnnouncementRequest,
                               session: SessionDependency):
    announcement_dict = announcement_data.model_dump(exclude_unset=True)
    announcement_orm_obj = await CRUD.get_item_by_id(session, models.Announcement, announcement_id)

    for field, value in announcement_dict.items():
        setattr(announcement_orm_obj, field, value)
    await CRUD.add_item(session, announcement_orm_obj)
    return SUCCESS_RESPONSE

@app.delete('/announcements/{announcement_id}', response_model=DeleteAnnouncementResponse)
async def get_announcements(announcement_id: int, session: SessionDependency):
    announcement_orm_obj = await CRUD.get_item_by_id(session, models.Announcement, announcement_id)
    await CRUD.delete_item(session, announcement_orm_obj)
    return SUCCESS_RESPONSE

