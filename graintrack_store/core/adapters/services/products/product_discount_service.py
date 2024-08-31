from datetime import datetime
from decimal import Decimal
from types import EllipsisType
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import NotFound

from graintrack_store.core.adapters.repositories.products.product_discount_repository import ProductDiscountRepository
from graintrack_store.core.adapters.repositories.products.product_repository import ProductRepository
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.products.product_discount_validator import ProductDiscountValidator
from graintrack_store.products.models import ProductDiscount


class ProductDiscountService(BaseService):
    product_discount_repository: ProductDiscountRepository
    product_discount_validator: ProductDiscountValidator

    def __init__(self):
        self.product_discount_repository = ProductDiscountRepository()
        self.repository = self.product_discount_repository

        product_repository = ProductRepository()
        self.product_discount_validator = ProductDiscountValidator(
            product_repository=product_repository
        )

    def create_product_discount(
        self,
        product_uuid: UUID,
        discount_started_at: datetime,
        discount_ended_at: datetime,
        discount_percentage: Decimal,
    ) -> ProductDiscount:
        with transaction.atomic():
            validated_data = self.product_discount_validator.validate_create(
                product_uuid=product_uuid,
                discount_started_at=discount_started_at,
                discount_ended_at=discount_ended_at,
                discount_percentage=discount_percentage
            )
            product_discount = self.product_discount_repository.create(
                **validated_data.dict(exclude_unset=True)
            )
        return product_discount

    def update_product_discount(
        self,
        instance_uuid: UUID,
        discount_started_at: datetime | EllipsisType = ...,
        discount_ended_at: datetime | EllipsisType = ...,
        discount_percentage: Decimal | EllipsisType = ...,
        is_active: bool | EllipsisType = ...,
    ) -> ProductDiscount:
        with transaction.atomic():
            instance = self.product_discount_repository.retrieve_by_uuid(instance_uuid=instance_uuid)
            if not instance:
                raise NotFound("Order object not found")

            validated_data = self.product_discount_validator.validate_update(
                discount_started_at=discount_started_at,
                discount_ended_at=discount_ended_at,
                discount_percentage=discount_percentage,
                is_active=is_active
            )
            product_discount = self.product_discount_repository.update(
                instance, **validated_data.dict(exclude_unset=True)
            )
        return product_discount

