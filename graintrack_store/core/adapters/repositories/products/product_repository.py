from decimal import Decimal
from types import EllipsisType

from graintrack_store.core.adapters.filters.products.product_filters import ProductFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.products.models import Product


class ProductRepository(BaseRepository):
    model = Product
    filterset = ProductFilterSet

    def create(
        self,
        is_deleted: bool,
        name: str,
        category_id: int,
        price: Decimal,
        description:str,
        available_quantity: int,
    ) -> Product:
        data = {
            "is_deleted": is_deleted,
            "name": name,
            "category_id": category_id,
            "price": price,
            "description": description,
            "available_quantity": available_quantity,
        }
        product = Product(**data)
        product.save()
        return product

    def update(
        self,
        instance: Product,
        is_deleted: bool | EllipsisType = ...,
        name: str | EllipsisType = ...,
        category_id: int | EllipsisType = ...,
        price: Decimal | EllipsisType = ...,
        description: str | EllipsisType = ...,
        available_quantity: int | EllipsisType = ...,
    ) -> Product:
        data = {
            "is_deleted": is_deleted,
            "name": name,
            "category_id": category_id,
            "price": price,
            "description": description,
            "available_quantity": available_quantity,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data:
            setattr(instance, field, value)

        instance.save()
        return instance
