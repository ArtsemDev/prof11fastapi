from sqlalchemy import Column, DECIMAL, VARCHAR, BOOLEAN, INT, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Category(Base):
    name = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    slug = Column(VARCHAR(64), nullable=False, unique=True, index=True)

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return self.name


class Product(Base):
    name = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    slug = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    description = Column(VARCHAR(1024), nullable=True)
    price = Column(DECIMAL(6, 2), nullable=False)
    is_published = Column(BOOLEAN, default=False)
    category_id = Column(INT, ForeignKey('category.id', ondelete='RESTRICT'), nullable=False)

    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return self.name
