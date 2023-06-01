from fastapi import FastAPI
import asyncio
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete

from src.router import router
from src.models import Category, Product
from src.schemas import CategoryDetail


app = FastAPI(title='BELHARD', description='PROF 11')
app.include_router(router=router)


async def main():
    async with Category.async_session() as session:
        cat = await session.get(Category, 1, options=[selectinload(Category.products)])
        schema = CategoryDetail.from_orm(cat)
        print(schema)
        # objs = await session.execute(
        #     select(Category, Product)
        #     .join(Product)
        #     .filter(Product.is_published)
        # )
        # print(objs.all())
        # objs = await session.scalars(
        #     select(Category)
        #     .order_by(Category.name.desc())
        # )
        # print(objs.all())
        # await session.execute(
        #     update(Product)
        #     .values(name='')
        #     .where(Product.id == 2)
        # )
        # await session.execute(
        #     delete(Product).filter(Product.id >= 2)
        # )
        # await session.commit()
        # cappuccino = await session.get(Product, 1, options=[selectinload(Product.category)])
        # await session.delete(cappuccino)
        # await session.commit()
        # cappuccino.name = 'Капучино'
        # session.add(cappuccino)
        # await session.commit()
        # print(cappuccino.name)
        # print(cappuccino.category.slug)
        # coffee = Category(name='Кофе', slug='coffee')
        # pancakes = Category(name='Панкейки', slug='pancakes')
        # cappuccino = Product(
        #     name='Капучино S',
        #     slug='cappuccino-s',
        #     description='100% арабика',
        #     price=5,
        #     is_published=True,
        #     category_id=1
        # )
        # session.add_all([coffee, pancakes, cappuccino])
        # await session.commit()
        # await session.refresh(coffee, attribute_names=['products', 'id'])
        # await session.refresh(pancakes, attribute_names=['products', 'id'])
        # await session.refresh(cappuccino, attribute_names=['category'])
        # print(coffee.products)
        # print(cappuccino.category)


# asyncio.run(main())
