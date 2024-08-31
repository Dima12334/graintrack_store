from decimal import Decimal
from types import EllipsisType

from graintrack_store.core.adapters.filters.orders.order_filters import OrderFilterSet
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.models import Order


class OrderRepository(BaseRepository):
    model = Order
    filterset = OrderFilterSet

    def create(
        self,
        creator_id: int,
        status: str,
        order_code: str,
        comment: str,
        total_sum: Decimal,
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
