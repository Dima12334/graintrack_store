from types import EllipsisType
from typing import Optional
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import NotFound

from graintrack_store.core.adapters.repositories.products.product_category_repository import ProductCategoryRepository
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.products.product_category_validator import ProductCategoryValidator
from graintrack_store.products.models import ProductCategory


class ProductCategoryService(BaseService):
    product_category_repository: ProductCategoryRepository
    product_category_validator: ProductCategoryValidator

    def __init__(self):
        self.product_category_repository = ProductCategoryRepository()
        self.repository = self.product_category_repository

        self.product_category_validator = ProductCategoryValidator(
            product_category_repository=self.product_category_repository
        )

    def create_product_category(
        self,
        name: str,
        description: str = "",
        parent_category_uuid: Optional[UUID] = None,
    ) -> ProductCategory:
        with transaction.atomic():
            validated_data = self.product_category_validator.validate_create(
                name=name,
                description=description,
                parent_category_uuid = parent_category_uuid,
            )
            parent_category = self.product_category_repository.create(
                **validated_data.dict(exclude_unset=True)
            )
        return parent_category

    def update_product_category(
        self,
        instance_uuid: UUID,
        name: str | EllipsisType = ...,
        description: str | EllipsisType = ...,
    ) -> ProductCategory:
        with transaction.atomic():
            instance = self.product_category_repository.retrieve_by_uuid(instance_uuid=instance_uuid)
            if not instance:
                raise NotFound("Product category object not found")

            validated_data = self.product_category_validator.validate_update(
                name=name,
                description=description
            )
            parent_category = self.product_category_repository.update(
                instance, **validated_data.dict(exclude_unset=True)
            )
        return parent_category
