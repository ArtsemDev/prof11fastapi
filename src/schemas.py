from typing import Optional, List

from pydantic import BaseModel, Field, PositiveInt, root_validator, BaseSettings, PostgresDsn
from pydantic.types import Decimal
import ujson
from slugify import slugify


# from .types import MysqlDsn


class ProductForm(BaseModel):
    name: str = Field(
        ...,
        max_length=64,
        title='Product Name',
    )
    slug: str = Field(
        ...,
        max_length=64
    )
    description: Optional[str] = Field(max_length=1024)
    is_published: bool = Field(default=False)
    price: Decimal = Field(..., max_digits=6, decimal_places=2)
    category_id: PositiveInt = Field(...)


class ProductDetail(ProductForm):
    id: Optional[PositiveInt]

    class Config:
        orm_mode = True


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
    slug: Optional[str] = Field(
        ...,
        max_length=64,
        title='Category URL',
        description='Unique Category URL'
    )
    products: Optional[List[ProductDetail]]

    @root_validator(pre=True)
    def validator(cls, values: dict) -> dict:
        if not values.get('slug'):
            values['slug'] = slugify(values.get('name'))
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


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = '.env'
