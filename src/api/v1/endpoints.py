from typing import List

from .router import router
from src.schemas import CategoryForm, CategoryDetail


categories = [
    {'id': 1, 'name': 'Coffee', 'slug': 'coffee'},
    {'id': 2, 'name': 'Tea', 'slug': 'tea'},
]


@router.get('/category', response_model=List[CategoryDetail], tags=['Category'], name='category list')
async def category_list():
    return [CategoryDetail(**category) for category in categories]


@router.post('/category', response_model=CategoryDetail, tags=['Category'], name='add_category')
async def add_category(category: CategoryForm):
    category = CategoryDetail(**category.dict())
    max_id = max(categories, key=lambda x: x.get('id'))
    category.id = max_id['id'] + 1
    categories.append(category.dict())
    return category
