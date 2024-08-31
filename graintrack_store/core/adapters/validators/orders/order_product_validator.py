from decimal import Decimal
from types import EllipsisType

from django.utils import timezone
from pydantic import ValidationError

from graintrack_store.core.adapters.repositories.orders.order_product_repository import OrderProductRepository
from graintrack_store.core.adapters.repositories.orders.order_repository import OrderRepository
from graintrack_store.core.adapters.repositories.products.product_discount_repository import ProductDiscountRepository
from graintrack_store.core.adapters.repositories.products.product_repository import ProductRepository
from graintrack_store.core.adapters.schemas.orders.order_product_schemas import (
    OrderProductUpdateSchema, OrderProductCreateOutSchema, OrderProductCreateInSchema)
from uuid import UUID

from graintrack_store.core.utils import remove_ellipsis_fields


class OrderProductValidator:
    order_repository: OrderRepository
    product_repository: ProductRepository
    product_discount_repository: ProductDiscountRepository

    def __init__(
        self,
        order_repository: OrderRepository,
        order_product_repository: OrderProductRepository,
        product_repository: ProductRepository,
        product_discount_repository: ProductDiscountRepository,
    ):
        self.order_repository = order_repository
        self.order_product_repository = order_product_repository
        self.product_repository = product_repository
        self.product_discount_repository = product_discount_repository

    def validate_create(
        self,
        order_uuid: UUID,
        product_uuid: UUID,
        quantity: int,
    ) -> OrderProductCreateOutSchema:
        data = {
            "order_uuid": order_uuid,
            "product_uuid": product_uuid,
            "quantity": quantity,
        }
        schema = OrderProductCreateInSchema(**data)

        order = self.order_repository.retrieve_by_uuid(instance_uuid=schema.order_uuid)
        if not order:
            raise ValidationError(f"Order with uuid {schema.order_uuid} not found.")
        product = self.product_repository.retrieve_by_uuid(instance_uuid=schema.product_uuid)
        if not product:
            raise ValidationError(f"Product with uuid {schema.product_uuid} not found.")

        order_product_already_exists = self.order_product_repository.check_existence_by_order_and_product(
            order_id=order.id, product_id=product.id
        )
        if order_product_already_exists:
            raise ValidationError(
                f"Product with uuid {schema.product_uuid} already added to order with uuid {schema.order_uuid}."
            )

        if product.available_quantity < schema.quantity:
            raise ValidationError(
                f"Product available quantity less than specified quantity ({product.available_quantity}<{schema.quantity})."
            )

        product_discount = self.product_discount_repository.get_discount_by_product_uuid(
            product_uuid=product.uuid
        )
        if (
            product_discount
            and product_discount.is_active
            and product_discount.discount_started_at <= timezone.now() <= product_discount.discount_ended_at
        ):
            discount = (product_discount.discount_percentage / Decimal("100.0")) * product.price
        else:
            discount = Decimal(0)

        out_data = schema.dict(exclude_unset=True)
        out_data["order_id"] = order.id
        out_data["product_id"] = product.id
        out_data["price"] = product.price
        out_data["discount"] = discount

        return OrderProductCreateOutSchema(**out_data)

    def validate_update(
        self,
        quantity: int | EllipsisType = ...
    ) -> OrderProductUpdateSchema:
        data = {
            "quantity": quantity,
        }
        data = remove_ellipsis_fields(data)
        schema = OrderProductUpdateSchema(**data)

        return schema
