from decimal import Decimal
from types import EllipsisType
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound

from graintrack_store.core.adapters.repositories.orders.order_product_repository import (
    OrderProductRepository,
)
from graintrack_store.core.adapters.repositories.orders.order_repository import (
    OrderRepository,
)
from graintrack_store.core.adapters.repositories.products.product_discount_repository import (
    ProductDiscountRepository,
)
from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.orders.order_product_validator import (
    OrderProductValidator,
)
from graintrack_store.core.constants import DECIMAL_PLACES
from graintrack_store.orders.models import OrderProduct


class OrderProductService(BaseService):
    order_product_repository: OrderProductRepository
    order_repository: OrderRepository
    product_repository: ProductRepository
    order_product_validator: OrderProductValidator

    def __init__(self):
        self.order_product_repository = OrderProductRepository()
        self.repository = self.order_product_repository

        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        product_discount_repository = ProductDiscountRepository()
        self.order_product_validator = OrderProductValidator(
            order_repository=self.order_repository,
            order_product_repository=self.order_product_repository,
            product_repository=self.product_repository,
            product_discount_repository=product_discount_repository,
        )

    def create_order_product(
        self,
        order_uuid: UUID,
        product_uuid: UUID,
        quantity: int,
    ) -> OrderProduct:
        with transaction.atomic():
            validated_data = self.order_product_validator.validate_create(
                order_uuid=order_uuid,
                product_uuid=product_uuid,
                quantity=quantity,
            )

            order_product = self.order_product_repository.create(
                **validated_data.dict(exclude_unset=True)
            )

            order = self.order_repository.retrieve_by_uuid(instance_uuid=order_uuid)
            new_total_sum = round(
                order.total_sum
                + Decimal(
                    order_product.quantity
                    * (order_product.price - order_product.discount)
                ),
                DECIMAL_PLACES,
            )
            self.order_repository.update(instance=order, total_sum=new_total_sum)

            self.product_repository.decrease_available_quantity(
                product_id=order_product.product_id, quantity=order_product.quantity
            )
        return order_product

    def update_order_product(
        self, instance_uuid: UUID, quantity: int | EllipsisType = ...
    ) -> OrderProduct:
        with transaction.atomic():
            instance = self.order_product_repository.retrieve_by_uuid(
                instance_uuid=instance_uuid
            )
            if not instance:
                raise NotFound("Order product object not found")

            validated_data = self.order_product_validator.validate_update(
                quantity=quantity,
            )
            order = self.order_repository.retrieve_by_id(instance_id=instance.order_id)
            old_order_product_quantity = instance.quantity
            old_order_product_sum = instance.quantity * (
                instance.price - instance.discount
            )

            order_product = self.order_product_repository.update(
                instance, **validated_data.dict(exclude_unset=True)
            )
            new_order_product_sum = order_product.quantity * (
                order_product.price - order_product.discount
            )
            sum_change = new_order_product_sum - old_order_product_sum
            new_total_sum = round(order.total_sum + sum_change, DECIMAL_PLACES)
            self.order_repository.update(instance=order, total_sum=new_total_sum)

            if old_order_product_quantity < order_product.quantity:
                self.product_repository.decrease_available_quantity(
                    product_id=order_product.product_id,
                    quantity=order_product.quantity - old_order_product_quantity,
                )
            else:
                self.product_repository.increase_available_quantity(
                    product_id=order_product.product_id,
                    quantity=old_order_product_quantity - order_product.quantity,
                )

        return order_product

    def delete_order_product(self, instance_uuid: UUID) -> None:
        with transaction.atomic():
            instance = self.order_repository.retrieve_by_uuid(
                instance_uuid=instance_uuid
            )
            if not instance:
                raise NotFound("Order product object not found")

            order = self.order_repository.retrieve_by_id(instance_id=instance.order_id)
            new_total_sum = round(
                order.total_sum
                - Decimal(instance.quantity * (instance.price - instance.discount)),
                DECIMAL_PLACES,
            )
            self.order_repository.update(instance=order, total_sum=new_total_sum)

            self.product_repository.increase_available_quantity(
                product_id=instance.product_id, quantity=instance.quantity
            )

            deleted = self.order_product_repository.delete(instance_uuid=instance_uuid)
            if not deleted:
                raise ValidationError("Failed to delete order product.")
