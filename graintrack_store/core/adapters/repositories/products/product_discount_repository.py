from datetime import datetime
from decimal import Decimal
from types import EllipsisType
from typing import Optional
from uuid import UUID

from graintrack_store.core.adapters.filters.products.product_discount_filters import (
    ProductDiscountFilterSet,
)
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.products.models import ProductDiscount


class ProductDiscountRepository(BaseRepository):
    model = ProductDiscount
    filterset = ProductDiscountFilterSet

    def get_base_qs(self):
        return ProductDiscount.objects.select_related("product").all()

    def create(
        self,
        product_id: int,
        discount_started_at: datetime,
        discount_ended_at: datetime,
        discount_percentage: Decimal,
        is_active: bool = True,
    ) -> ProductDiscount:
        data = {
            "product_id": product_id,
            "discount_started_at": discount_started_at,
            "discount_ended_at": discount_ended_at,
            "discount_percentage": discount_percentage,
            "is_active": is_active,
        }
        product_discount = ProductDiscount(**data)
        product_discount.save()
        return product_discount

    def update(
        self,
        instance: ProductDiscount,
        discount_started_at: datetime | EllipsisType = ...,
        discount_ended_at: datetime | EllipsisType = ...,
        discount_percentage: Decimal | EllipsisType = ...,
        is_active: bool | EllipsisType = ...,
    ) -> ProductDiscount:
        data = {
            "discount_started_at": discount_started_at,
            "discount_ended_at": discount_ended_at,
            "discount_percentage": discount_percentage,
            "is_active": is_active,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    def get_discount_by_product_uuid(
        self, product_uuid: UUID
    ) -> Optional[ProductDiscount]:
        return ProductDiscount.objects.filter(product__uuid=product_uuid).first()
