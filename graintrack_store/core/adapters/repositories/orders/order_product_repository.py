from decimal import Decimal
from types import EllipsisType
from typing import Dict, List, Any, Optional
from uuid import UUID

from django.db.models import F

from graintrack_store.core.adapters.filters.orders.order_product_filters import (
    OrderProductFilterSet,
)
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.orders.models import OrderProduct
from graintrack_store.users.models import User


class OrderProductRepository(BaseRepository):
    model = OrderProduct
    filterset = OrderProductFilterSet

    def get_base_qs(self):
        return OrderProduct.objects.select_related(
            "order",
            "order__creator",
            "product",
            "product__category",
        ).all()

    def create(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        price: Decimal,
        discount: Decimal,
    ) -> OrderProduct:
        data = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "discount": discount,
        }
        order = OrderProduct(**data)
        order.save()
        return order

    def update(
        self,
        instance: OrderProduct,
        quantity: int | EllipsisType = ...,
    ) -> OrderProduct:
        data = {
            "quantity": quantity,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    def retrieve_by_uuid(self, instance_uuid: UUID) -> Optional[OrderProduct]:
        queryset = self.get_base_qs()
        queryset = queryset.annotate(price_with_discount=F("price") - F("discount"))
        queryset = queryset.filter(uuid=instance_uuid)
        return queryset.first()

    def list(self, filters: Dict[str, Any] = None) -> List[OrderProduct]:
        queryset = self.get_base_qs()
        queryset = queryset.annotate(price_with_discount=F("price") - F("discount"))

        if self.filterset and filters:
            filterset = self.filterset(filters, queryset)
            filterset.is_valid()
            queryset = filterset.qs
        queryset = queryset.order_by(self.default_ordering)

        return list(queryset)

    def list_by_order_creator(
        self, creator: User, filters: Dict[str, Any] = None
    ) -> List[OrderProduct]:
        queryset = self.get_base_qs()
        queryset = queryset.filter(order__creator=creator).annotate(
            price_with_discount=F("price") - F("discount")
        )

        if self.filterset and filters:
            filterset = self.filterset(filters, queryset)
            filterset.is_valid()
            queryset = filterset.qs
        queryset = queryset.order_by(self.default_ordering)

        return list(queryset)

    def check_existence_by_order_and_product(
        self, order_id: int, product_id: int
    ) -> bool:
        return OrderProduct.objects.filter(
            order_id=order_id, product_id=product_id
        ).exists()
