from typing import Type

from fastapi import Path
from sqlalchemy import Column, INT
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .settings import SETTINGS


class Base(DeclarativeBase):

    id = Column(INT, primary_key=True)  # autoincrement=True for sqlite3

    _async_engine = create_async_engine(
        SETTINGS.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
        # FOR MYSQL DATABASE
        # SETTINGS.DATABASE_URL.replace('mysql+mysqlconnector://', 'mysql+aiomysql://')
    )
    async_session = async_sessionmaker(bind=_async_engine)

    @declared_attr
    def __tablename__(cls):
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

    @classmethod
    async def get(cls, pk: int = Path(ge=1)) -> Type["Base"]:
        async with Base.async_session() as session:
            return await session.get(cls, pk)

    async def delete(self):
        async with self.async_session() as session:
            await session.delete(self)
            await session.commit()

    async def save(self):
        async with self.async_session() as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
