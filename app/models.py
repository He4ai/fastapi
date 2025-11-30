import datetime

import config
from sqlalchemy import DateTime, Integer, String, Float, func
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {'id': self.id}

class Announcement(Base):
    __tablename__ = 'announcement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    autor: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'price': self.price,
            'creation_date': self.creation_date.isoformat(),
            'autor': self.autor,
        }

ORM_OBJ = Announcement
ORM_CLS = type(Announcement)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("PG_DSN =", config.PG_DSN)


async def close_orm():
    await engine.dispose()