from decimal import Decimal
from types import EllipsisType
from typing import Dict, Any, List

from graintrack_store.core.adapters.filters.orders.order_filters import OrderFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.models import Order
from graintrack_store.users.models import User


class OrderRepository(BaseRepository):
    model = Order
    filterset = OrderFilterSet

    def get_base_qs(self):
        return Order.objects.select_related("creator").all()

    def create(
        self,
        creator_id: int,
        status: str,
        order_code: str,
        total_sum: Decimal,
        comment: str = "",
    ) -> Order:
        data = {
            "creator_id": creator_id,
            "status": status,
            "order_code": order_code,
            "comment": comment,
            "total_sum": total_sum,
        }
        order = Order(**data)
        order.save()
        return order

    def update(
        self,
        instance: Order,
        status: str | EllipsisType = ...,
        comment: str | EllipsisType = ...,
        total_sum: Decimal | EllipsisType = ...,
    ) -> Order:
        data = {
            "status": status,
            "comment": comment,
            "total_sum": total_sum,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data:
            setattr(instance, field, value)

        instance.save()
        return instance

    def list_by_creator(self, creator: User, filters: Dict[str, Any] = None) -> List[Order]:
        queryset = self.get_base_qs()
        queryset = queryset.filter(creator=creator)

        if self.filterset and filters:
            filterset = self.filterset(filters, queryset)
            filterset.is_valid()
            queryset = filterset.qs
        queryset = queryset.order_by(self.default_ordering)

        return list(queryset)

    def check_existence_by_order_code(self, order_code: str) -> bool:
        return Order.objects.filter(order_code=order_code).exists()
