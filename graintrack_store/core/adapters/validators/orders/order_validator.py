from types import EllipsisType

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.orders.order_product_repository import (
    OrderProductRepository,
)
from graintrack_store.core.adapters.repositories.orders.order_repository import (
    OrderRepository,
)
from graintrack_store.core.adapters.schemas.orders.order_schemas import (
    OrderCreateSchema,
    OrderUpdateSchema,
)
from graintrack_store.core.adapters.validators.base import BaseValidator
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.orders.models import Order
from pydantic import ValidationError as PydanticValidationError


class OrderValidator(BaseValidator):
    order_repository: OrderRepository
    order_product_repository: OrderProductRepository

    def __init__(
        self,
        order_repository: OrderRepository,
        order_product_repository: OrderProductRepository,
    ):
        self.order_repository = order_repository
        self.order_product_repository = order_product_repository

    def validate_order_already_exists(self, order_code: str) -> None:
        order_already_exists = self.order_repository.check_existence_by_order_code(
            order_code=order_code
        )
        if order_already_exists:
            raise ValidationError(
                f"Order with such order code {order_code} already exists."
            )

    def validate_change_order_status_to_sold(
        self, order: Order, new_status: str
    ) -> None:
        order_products = self.order_product_repository.get_order_products_by_order_uuid(
            order_uuid=order.uuid
        )
        if not order_products:
            raise ValidationError(
                f"You cannot change order status to {new_status} without specified products in order."
            )

    def validate_create_order(
        self,
        status: str,
        order_code: str,
        comment: str = "",
    ) -> OrderCreateSchema:
        data = {
            "status": status,
            "order_code": order_code,
            "comment": comment,
        }
        try:
            schema = OrderCreateSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        self.validate_order_already_exists(order_code=schema.order_code)

        return schema

    def validate_update_order(
        self,
        instance: Order,
        status: str | EllipsisType = ...,
        comment: str | EllipsisType = ...,
    ) -> OrderUpdateSchema:
        data = {
            "status": status,
            "comment": comment,
        }
        data = remove_ellipsis_fields(data)
        try:
            schema = OrderUpdateSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        if schema.status and schema.status == OrderConstants.STATUS_CHOICE.SOLD:
            self.validate_change_order_status_to_sold(
                order=instance, new_status=schema.status
            )
            schema.sold_at = timezone.now()

        return schema

    def validate_delete_order(self, instance: Order) -> None:
        sold_order_status = OrderConstants.STATUS_CHOICE.SOLD
        if instance.status == sold_order_status:
            raise ValidationError(
                f"You cannot delete order in {sold_order_status} status."
            )
