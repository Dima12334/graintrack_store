from graintrack_store.core.adapters.filters.products.product_filters import ProductFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.products.models import Product


class ProductRepository(BaseRepository):
    model = Product
    filterset = ProductFilterSet
