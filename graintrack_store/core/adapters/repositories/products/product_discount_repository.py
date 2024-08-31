from graintrack_store.core.adapters.filters.products.product_discount_filters import ProductDiscountFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.products.models import ProductDiscount


class ProductDiscountRepository(BaseRepository):
    model = ProductDiscount
    filterset = ProductDiscountFilterSet
