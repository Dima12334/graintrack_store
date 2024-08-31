from types import EllipsisType

from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.schemas.orders.order_schemas import OrderCreateSchema, OrderUpdateSchema
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.orders.models import Order


class OrderValidator:

    def validate_create(
        self,
        status: str,
        order_code: str,
        comment: str,
    ) -> OrderCreateSchema:
        data = {
            "status": status,
            "order_code": order_code,
            "comment": comment,
        }
        schema = OrderCreateSchema(**data)
        return schema

    def validate_update(
        self,
        status: str | EllipsisType = ...,
        comment: str | EllipsisType = ...,
    ) -> OrderUpdateSchema:
        data = {
            "status": status,
            "comment": comment,
        }
        data = remove_ellipsis_fields(data)
        schema = OrderUpdateSchema(**data)
        return schema

    def validate_delete(self, instance: Order) -> None:
        sold_order_status = OrderConstants.STATUS_CHOICE.SOLD
        if instance.status == sold_order_status:
            raise ValidationError(f"You cannot delete order in {sold_order_status} status.")
