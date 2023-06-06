from fastapi import HTTPException, status, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.models import Category
from src.schemas import CategoryForm, CategoryDetail, CategoryDetailFull
from .router import router
from .types import CategoryPageNumberPaginator


# @router.get(
#     '/category',
#     response_model=List[CategoryDetail],
#     tags=['Category'],
#     response_model_exclude_none=True,
#     name='category list'
# )
# async def category_list(limit: int = Query(default=5, ge=1), offset: int = Query(default=0, ge=0)):
#     async with Category.async_session() as session:
#         categories = await session.scalars(
#             select(Category)
#             .order_by(Category.id.asc())
#             .limit(limit)
#             .offset(offset)
#         )
#         categories = categories.all()
#         if categories:
#             return [CategoryDetail(
#                 id=category.id,
#                 name=category.name,
#                 slug=category.slug,
#             ) for category in categories]
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='page not found')

# Content-Type
@router.get(
    '/category',
    response_model=CategoryPageNumberPaginator,
    tags=['Category'],
    response_model_exclude_none=True,
    name='category list'
)
async def category_list(
        response: JSONResponse,
        data: CategoryPageNumberPaginator = Depends(CategoryPageNumberPaginator.page)
):
    response.headers['My-Header'] = 'My Value'
    return data
    # async with Category.async_session() as session:
    #     categories = await session.scalars(
    #         select(Category)
    #         .order_by(Category.id.asc())
    #         .limit(5)
    #         .offset(page * 5 - 5)
    #     )
    #     categories = categories.all()
    #     if categories:
    #         return [CategoryDetail(
    #             id=category.id,
    #             name=category.name,
    #             slug=category.slug,
    #         ) for category in categories]
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='page not found')


@router.post(
    '/category',
    response_model=CategoryDetail,
    tags=['Category'],
    response_model_exclude_none=True,
    name='add_category'
)
async def add_category(category: CategoryForm):
    category = Category(**CategoryDetail(**category.dict()).dict(exclude_none=True))
    try:
        await category.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name or slug is not unique')
    else:
        return CategoryDetail(
            id=category.id,
            name=category.name,
            slug=category.slug,
        )


@router.patch(
    path='/category/{pk}',
    tags=['Category'],
    response_model=CategoryDetail,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    name='edit_category'
)
async def edit_category(category: CategoryForm, obj: Category = Depends(Category.get)):
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
    category = CategoryDetail(**category.dict())
    obj.name = category.name
    obj.slug = category.slug
    try:
        await obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category name and slug must be unique')
    else:
        category.id = obj.id
        return category


@router.get(
    path='/category/{pk}',
    response_model=CategoryDetail,
    response_model_exclude_none=True,
    tags=['Category'],
    name='category_detail'
)
async def category_detail(category: Category = Depends(Category.get)):
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
    return CategoryDetail.from_orm(category)


@router.delete(
    path='/category/{pk}',
    tags=['Category'],
    name='delete_category'
)
async def delete_category(category: Category = Depends(Category.get)):
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
    await category.delete()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='category was deleted')


@router.get(
    path='/category/{category_id}/product',
    response_model=CategoryDetailFull,
    tags=['Category'],
    name='category products'
)
async def category_detail(category_id: int = Path(ge=1)):
    async with Category.async_session() as session:
        category = await session.get(Category, category_id, options=[selectinload(Category.products)])
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        return CategoryDetailFull.from_orm(category)
