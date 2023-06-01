from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path

from .router import router
from src.schemas import CategoryForm, CategoryDetail
from src.models import Category


@router.get(
    '/category',
    response_model=List[CategoryDetail],
    tags=['Category'],
    response_model_exclude_none=True,
    name='category list'
)
async def category_list():
    async with Category.async_session() as session:
        categories = await session.scalars(select(Category).order_by(Category.id.asc()))
        return [CategoryDetail(
            id=category.id,
            name=category.name,
            slug=category.slug,
        ) for category in categories]


@router.post(
    '/category',
    response_model=CategoryDetail,
    tags=['Category'],
    response_model_exclude_none=True,
    name='add_category'
)
async def add_category(category: CategoryForm):
    category = Category(**CategoryDetail(**category.dict()).dict(exclude_none=True))
    async with Category.async_session() as session:
        session.add(category)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name or slug is not unique')
        else:
            await session.refresh(category)
            return CategoryDetail(
                id=category.id,
                name=category.name,
                slug=category.slug,
            )


@router.patch(
    path='/category/{category_id}',
    tags=['Category'],
    response_model=CategoryDetail,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    name='edit_category'
)
async def edit_category(category: CategoryForm, category_id: int = Path(ge=1)):
    async with Category.async_session() as session:
        obj = await session.get(Category, category_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        category = CategoryDetail(**category.dict())
        obj.name = category.name
        obj.slug = category.slug
        session.add(obj)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name and slug must be unique')
        else:
            category.id = category_id
            return category


@router.get(
    path='/category/{category_id}',
    response_model=CategoryDetail,
    response_model_exclude_none=True,
    tags=['Category'],
    name='category_detail'
)
async def category_detail(category_id: int = Path(ge=1)):
    async with Category.async_session() as session:
        category = await session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        return CategoryDetail(
            id=category.id,
            name=category.name,
            slug=category.slug,
        )


@router.delete(
    path='/category/{category_id}',
    tags=['Category'],
    name='delete_category'
)
async def delete_category(category_id: int = Path(ge=1)):
    async with Category.async_session() as session:
        obj = await session.get(Category, category_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        await session.delete(obj)
        await session.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='category was deleted')


@router.get(
    path='/category/{category_id}/product',
    response_model=CategoryDetail,
    tags=['Category'],
    name='category products'
)
async def category_detail(category_id: int = Path(ge=1)):
    async with Category.async_session() as session:
        category = await session.get(Category, category_id, options=[selectinload(Category.products)])
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        return CategoryDetail.from_orm(category)
