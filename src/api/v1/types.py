from src.models import Category
from src.schemas import CategoryDetail
from src.types.paginator.page_number import PageNumberPaginator


class CategoryPageNumberPaginator(PageNumberPaginator):
    __model__ = Category
    __schema__ = CategoryDetail
    __url__ = '/api/v1/category'
