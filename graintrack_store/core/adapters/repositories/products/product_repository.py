from decimal import Decimal
from types import EllipsisType
from typing import List, Iterable
from uuid import UUID

from django.db.models import F

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
    ) -> Product:
        data = {
            "is_deleted": is_deleted,
            "name": name,
            "category_id": category_id,
            "price": price,
            "description": description,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data:
            setattr(instance, field, value)

        instance.save()
        return instance

    def bulk_update(self, instances: Iterable[Product], fields: List[str], **kwargs) -> None:
        return Product.objects.bulk_update(instances, fields=fields, **kwargs)

    def get_products_by_ids(self, ids: Iterable[int]) -> List[Product]:
        queryset = Product.objects.filter(id__in=ids)
        return list(queryset)

    def increase_available_quantity(self, product_id: int, quantity: int) -> None:
        Product.objects.filter(id=product_id).update(
            available_quantity=F("available_quantity") + quantity
        )

    def decrease_available_quantity(self, product_id: int, quantity: int) -> None:
        Product.objects.filter(id=product_id).update(
            available_quantity=F("available_quantity") - quantity
        )
