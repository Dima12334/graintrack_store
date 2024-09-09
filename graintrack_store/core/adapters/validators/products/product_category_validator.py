from types import EllipsisType
from typing import Optional

from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.products.product_category_repository import (
    ProductCategoryRepository,
)
from graintrack_store.core.adapters.schemas.products.product_category_schemas import (
    ProductCategoryCreateOutSchema,
    ProductCategoryUpdateSchema,
    ProductCategoryCreateInSchema,
)
from uuid import UUID

from graintrack_store.core.adapters.validators.base import (
    BaseValidator,
    ProductCategoryValidationMixin,
)
from graintrack_store.core.utils import remove_ellipsis_fields
from pydantic import ValidationError as PydanticValidationError


class ProductCategoryValidator(ProductCategoryValidationMixin, BaseValidator):
    product_category_repository: ProductCategoryRepository

    def __init__(self, product_category_repository: ProductCategoryRepository):
        self.product_category_repository = product_category_repository

    def validate_create_product_category(
        self,
        name: str,
        description: str = "",
        parent_category_uuid: Optional[UUID] = None,
    ) -> ProductCategoryCreateOutSchema:
        data = {
            "parent_category_uuid": parent_category_uuid,
            "name": name,
            "description": description,
        }
        try:
            schema = ProductCategoryCreateInSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        if schema.parent_category_uuid:
            parent_category = self.validate_category(
                category_uuid=schema.parent_category_uuid
            )
            parent_category_id = parent_category.id
        else:
            parent_category_id = ...

        out_data = schema.dict(exclude_unset=True)
        out_data["parent_category_id"] = parent_category_id
        out_data = remove_ellipsis_fields(out_data)

        return ProductCategoryCreateOutSchema(**out_data)

    def validate_update_product_category(
        self,
        name: str | EllipsisType = ...,
        description: str | EllipsisType = ...,
    ) -> ProductCategoryUpdateSchema:
        data = {
            "name": name,
            "description": description,
        }
        data = remove_ellipsis_fields(data)
        try:
            schema = ProductCategoryUpdateSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        return schema
