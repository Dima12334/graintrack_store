from decimal import Decimal
from types import EllipsisType
from typing import Dict, Any
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import NotFound

from graintrack_store.core.adapters.repositories.products.product_category_repository import (
    ProductCategoryRepository,
)
from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.products.product_validator import (
    ProductValidator,
)
from graintrack_store.products.models import Product
from graintrack_store.users.constants import UserConstants
from graintrack_store.users.models import User


class ProductService(BaseService):
    product_repository: ProductRepository
    product_validator: ProductValidator

    def __init__(self):
        self.product_repository = ProductRepository()
        self.repository = self.product_repository

        product_category_repository = ProductCategoryRepository()
        self.product_validator = ProductValidator(
            product_category_repository=product_category_repository
        )

    def create_product(
        self,
        category_uuid: UUID,
        name: str,
        price: Decimal,
        description: str = "",
    ) -> Product:
        with transaction.atomic():
            validated_data = self.product_validator.validate_create_product(
                category_uuid=category_uuid,
                name=name,
                price=price,
                description=description,
            )
            product = self.product_repository.create(
                **validated_data.dict(exclude_unset=True)
            )
        return product

    def update_product(
        self,
        instance_uuid: UUID,
        category_uuid: UUID | EllipsisType = ...,
        is_deleted: bool | EllipsisType = ...,
        name: str | EllipsisType = ...,
        price: Decimal | EllipsisType = ...,
        description: str | EllipsisType = ...,
    ) -> Product:
        with transaction.atomic():
            instance = self.product_repository.retrieve_by_uuid(
                instance_uuid=instance_uuid
            )
            if not instance:
                raise NotFound("Product object not found")

            validated_data = self.product_validator.validate_update_product(
                category_uuid=category_uuid,
                is_deleted=is_deleted,
                name=name,
                price=price,
                description=description,
            )
            product = self.product_repository.update(
                instance, **validated_data.dict(exclude_unset=True)
            )
        return product

    def get_sold_products_report_data(self, filters: Dict[Any, Any]) -> Dict[str, Any]:
        report_data = self.product_repository.get_sold_products_report_data(
            filters=filters
        )
        return report_data
