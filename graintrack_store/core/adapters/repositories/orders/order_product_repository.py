from decimal import Decimal
from types import EllipsisType

from graintrack_store.core.adapters.filters.orders.order_product_filters import (
    OrderProductFilterSet,
)
from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.models import OrderProduct


class OrderProductRepository(BaseRepository):
    model = OrderProduct
    filterset = OrderProductFilterSet

    def get_base_qs(self):
        return OrderProduct.objects.select_related("order", "product").all()

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

        for field, value in data:
            setattr(instance, field, value)

        instance.save()
        return instance

    def check_existence_by_order_and_product(
        self, order_id: int, product_id: int
    ) -> bool:
        return OrderProduct.objects.filter(
            order_id=order_id, product_id=product_id
        ).exists()
