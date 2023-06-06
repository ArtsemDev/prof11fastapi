from math import ceil
from typing import Type, Optional, List, Tuple, Union

from fastapi import Query, HTTPException, status
from pydantic import BaseModel, PositiveInt
from sqlalchemy import Select, Column, select
from sqlalchemy.sql.functions import count

from src.database import Base
from src.settings import SETTINGS


class PageNumberPaginator(BaseModel):
    __model__: Type[Base]
    __schema__: Type[BaseModel]
    __filter__: Tuple = ()
    __order_by__: Union[Column, str] = 'id'
    __paginate_by__: int = SETTINGS.PAGINATE_BY
    __url__: str = '/'

    max_page: PositiveInt
    next_page: Optional[str]
    prev_page: Optional[str]
    objects: List

    @classmethod
    async def _count(cls) -> int:
        async with cls.__model__.async_session() as session:
            return await session.scalar(
                select(count(cls.__model__.id))
                .filter(*cls.__filter__)
            )

    @classmethod
    async def _get_queryset(cls, page: int):
        async with cls.__model__.async_session() as session:
            objs = await session.scalars(
                select(cls.__model__)
                .filter(*cls.__filter__)
                .order_by(cls.__order_by__)
                .limit(cls.__paginate_by__)
                .offset(cls.__paginate_by__ * page - cls.__paginate_by__)
            )
            return objs.all()

    @classmethod
    async def page(cls, page: int = Query(default=1, ge=1)):
        objs = await cls._get_queryset(page=page)
        objs_count = await cls._count()
        max_page = ceil(objs_count / cls.__paginate_by__)
        if objs:
            objs = [cls.__schema__.from_orm(obj) for obj in objs]
            return cls(
                max_page=max_page,
                objects=objs,
                prev_page=cls.__url__ + f'?page={page-1}' if page > 1 else None,
                next_page=cls.__url__ + f'?page={page+1}' if page < max_page else None
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='page not found')
