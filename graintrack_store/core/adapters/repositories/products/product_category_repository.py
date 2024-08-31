from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.products.models import ProductCategory


class ProductCategoryRepository(BaseRepository):
    model = ProductCategory
