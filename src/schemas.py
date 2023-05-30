from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator
import ujson


class CategoryForm(BaseModel):
    name: str = Field(
        ...,
        max_length=64,
        title='Category name',
        description='Unique Category Name'
    )

    class Config:
        json_dumps = ujson.dumps
        json_loads = ujson.loads
        title = 'Category'
        schema_extra = {
            'example': {'name': 'Category Name'}
        }


class CategoryDetail(CategoryForm):
    id: Optional[PositiveInt] = Field(
        title='Category ID',
        description='Unique Category ID'
    )
    slug: str = Field(
        ...,
        max_length=64,
        title='Category URL',
        description='Unique Category URL'
    )

    @root_validator(pre=True)
    def validator(cls, values: dict) -> dict:
        if not values.get('slug'):
            values['slug'] = values.get('name')
        return values

    class Config:
        json_dumps = ujson.dumps
        json_loads = ujson.loads
        title = 'Category'
        schema_extra = {
            'example': {
                 'id': 1,
                 'name': 'Category Name',
                 'slug': 'category-name',
            }
        }
        orm_mode = True
