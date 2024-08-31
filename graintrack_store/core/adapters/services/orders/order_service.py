from types import EllipsisType
from typing import List, Dict, Any
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from graintrack_store.core.adapters.repositories.orders.order_product_repository import (
    OrderProductRepository,
)
from graintrack_store.core.adapters.repositories.orders.order_repository import (
    OrderRepository,
)
from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.orders.order_validator import (
    OrderValidator,
)
from graintrack_store.orders.constants import OrderConstants
from graintrack_store.orders.models import Order
from graintrack_store.users.constants import UserConstants
from graintrack_store.users.models import User


class OrderService(BaseService):
    order_repository: OrderRepository
    order_product_repository: OrderProductRepository
    product_repository: ProductRepository
    order_validator: OrderValidator

    def __init__(self):
        self.order_repository = OrderRepository()
        self.repository = self.order_repository
        self.order_product_repository = OrderProductRepository()
        self.product_repository = ProductRepository()

        self.order_validator = OrderValidator(order_repository=self.order_repository)

    def create_order(
        self,
        creator: User,
        order_code: str,
        comment: str = "",
    ) -> Order:
        with transaction.atomic():
            validated_data = self.order_validator.validate_create(
                status=OrderConstants.STATUS_CHOICE.RESERVED,
                order_code=order_code,
                comment=comment,
            )
            order = self.order_repository.create(
                creator_id=creator.id, **validated_data.dict(exclude_unset=True)
            )
        return order

    def update_order(
        self,
        instance_uuid: UUID,
        status: str | EllipsisType = ...,
        comment: str | EllipsisType = ...,
    ) -> Order:
        with transaction.atomic():
            instance = self.order_repository.retrieve_by_uuid(
                instance_uuid=instance_uuid
            )
            if not instance:
                raise NotFound("Order object not found")

            validated_data = self.order_validator.validate_update(
                status=status, comment=comment
            )
            order = self.order_repository.update(
                instance, **validated_data.dict(exclude_unset=True)
            )
        return order

    def delete_order(self, instance_uuid: UUID) -> None:
        with transaction.atomic():
            instance = self.order_repository.retrieve_by_uuid(
                instance_uuid=instance_uuid
            )
            if not instance:
                raise NotFound("Order object not found")

            self.order_validator.validate_delete(instance=instance)

            order_products = self.order_product_repository.list(
                filters={"order": instance_uuid}
            )
            product_id_to_quantity_mapping = {
                order_product.product_id: order_product.quantity
                for order_product in order_products
            }
            products_to_cancel_reserve = self.product_repository.get_products_by_ids(
                ids=product_id_to_quantity_mapping.keys()
            )
            products_to_update = []
            for product in products_to_cancel_reserve:
                quantity_to_increase = product_id_to_quantity_mapping[product.id]
                product.available_quantity += quantity_to_increase
                products_to_update.append(product)

            self.product_repository.bulk_update(
                instances=products_to_update, fields=["available_quantity"]
            )

            deleted = self.order_repository.delete(instance_uuid=instance_uuid)
            if not deleted:
                raise ValidationError("Failed to delete order.")

    def list_orders(self, user: User, filters: Dict[str, Any] = None) -> List[Order]:
        if user.role == UserConstants.ROLE_CHOICE.MODERATOR:
            orders = self.order_repository.list(filters=filters)
        else:
            orders = self.order_repository.list_by_creator(
                creator=user, filters=filters
            )
        return orders
