from decimal import Decimal
from types import EllipsisType

from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.products.product_category_repository import (
    ProductCategoryRepository,
)
from graintrack_store.core.adapters.schemas.products.product_schemas import (
    ProductCreateOutSchema,
    ProductUpdateOutSchema,
    ProductCreateInSchema,
    ProductUpdateInSchema,
)
from uuid import UUID

from graintrack_store.core.adapters.validators.base import (
    BaseValidator,
    ProductCategoryValidationMixin,
)
from graintrack_store.core.utils import remove_ellipsis_fields
from pydantic import ValidationError as PydanticValidationError


class ProductValidator(ProductCategoryValidationMixin, BaseValidator):
    product_category_repository: ProductCategoryRepository

    def __init__(self, product_category_repository: ProductCategoryRepository):
        self.product_category_repository = product_category_repository

    def validate_create_product(
        self,
        category_uuid: UUID,
        name: str,
        price: Decimal,
        description: str = "",
        is_deleted: bool = False,
        available_quantity: int = 0,
    ) -> ProductCreateOutSchema:
        data = {
            "category_uuid": category_uuid,
            "name": name,
            "price": price,
            "description": description,
            "is_deleted": is_deleted,
            "available_quantity": available_quantity,
        }
        try:
            schema = ProductCreateInSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        category = self.validate_category(category_uuid=schema.category_uuid)

        out_data = schema.dict(exclude_unset=True)
        out_data["category_id"] = category.id

        return ProductCreateOutSchema(**out_data)

    def validate_update_product(
        self,
        category_uuid: UUID | EllipsisType = ...,
        is_deleted: bool | EllipsisType = ...,
        name: str | EllipsisType = ...,
        price: Decimal | EllipsisType = ...,
        description: str | EllipsisType = ...,
    ) -> ProductUpdateOutSchema:
        data = {
            "category_uuid": category_uuid,
            "is_deleted": is_deleted,
            "name": name,
            "price": price,
            "description": description,
        }
        data = remove_ellipsis_fields(data)
        try:
            schema = ProductUpdateInSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        if schema.category_uuid:
            category = self.validate_category(category_uuid=schema.category_uuid)
            category_id = category.id
        else:
            category_id = ...

        out_data = schema.dict(exclude_unset=True)
        out_data["category_id"] = category_id
        out_data = remove_ellipsis_fields(out_data)

        return ProductUpdateOutSchema(**out_data)
