from decimal import Decimal
from types import EllipsisType
from typing import List, Iterable, Dict, Any

from django.db.models import F

from graintrack_store.core.adapters.filters.products.product_filters import ProductFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository, ModelType
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.products.models import Product


class ProductRepository(BaseRepository):
    model = Product
    filterset = ProductFilterSet

    def get_base_qs(self):
        return Product.objects.select_related("category").all()

    def create(
        self,
        name: str,
        category_id: int,
        price: Decimal,
        is_deleted: bool = False,
        available_quantity: int = 0,
        description: str = "",
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

    def list(self, filters: Dict[str, Any] = None) -> List[Product]:
        queryset = self.get_base_qs()
        queryset = queryset.filter(available_quantity__gt=0)

        if self.filterset and filters:
            filterset = self.filterset(filters, queryset)
            filterset.is_valid()
            queryset = filterset.qs
        queryset = queryset.order_by(self.default_ordering)

        return list(queryset)

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
