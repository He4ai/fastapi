from fastapi import FastAPI
from sqlalchemy import select

import datetime
from schema import (CreateAdvertisementRequest, CreateAdvertisementResponse, DeleteAdvertisementResponse,
                    GetAdvertisementResponse, SearchAdvertisementResponse, UpdateAdvertisementRequest,
                    UpdateAdvertisementResponse)
from lifespan import lifespan
from dependency import SessionDependency
import CRUD
import models
from constant import SUCCESS_RESPONSE
from models import Session

app = FastAPI(
    title='Avito',
    description='otivA',
    lifespan=lifespan
)

@app.post('/advertisement', response_model=CreateAdvertisementResponse)
async def create_advertisement(advertisement: CreateAdvertisementRequest, session: SessionDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True, exclude={"creation_date"})
    advertisement_orm_obj = models.Advertisement(**advertisement_dict)
    await CRUD.add_item(session, advertisement_orm_obj)
    return advertisement_orm_obj.id_dict


@app.get('/advertisement/{advertisement_id}', response_model=GetAdvertisementResponse)
async def get_advertisements(advertisement_id: int, session: SessionDependency):
    advertisement_orm_obj = await CRUD.get_item_by_id(session, models.Advertisement, advertisement_id)
    return advertisement_orm_obj.dict

@app.get('/advertisement', response_model=SearchAdvertisementResponse)
async def search_advertisements(session: SessionDependency,
                               title: str | None = None,
                               content: str | None = None,
                               price: float | None = None,
                               author: str | None = None):
    filters = []
    if title is not None:
        filters.append(models.Advertisement.title == title)
    if content is not None:
        filters.append(models.Advertisement.content == content)
    if price is not None:
        filters.append(models.Advertisement.price == price)
    if author is not None:
        filters.append(models.Advertisement.author == author)

    query = select(models.Advertisement)
    if filters:
        query = query.where(*filters)
    query = query.limit(10000)

    advertisements = await session.scalars(query)
    return {'results': [advertisement.dict for advertisement in advertisements]}

@app.patch('/advertisement/{advertisement_id}', response_model=UpdateAdvertisementResponse)
async def update_advertisements(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest,
                               session: SessionDependency):
    advertisement_dict = advertisement_data.model_dump(exclude_unset=True)
    advertisement_orm_obj = await CRUD.get_item_by_id(session, models.Advertisement, advertisement_id)

    for field, value in advertisement_dict.items():
        setattr(advertisement_orm_obj, field, value)
    await CRUD.add_item(session, advertisement_orm_obj)
    return SUCCESS_RESPONSE

@app.delete('/advertisement/{advertisement_id}', response_model=DeleteAdvertisementResponse)
async def delete_advertisements(advertisement_id: int, session: SessionDependency):
    advertisement_orm_obj = await CRUD.get_item_by_id(session, models.Advertisement, advertisement_id)
    await CRUD.delete_item(session, advertisement_orm_obj)
    return SUCCESS_RESPONSE

