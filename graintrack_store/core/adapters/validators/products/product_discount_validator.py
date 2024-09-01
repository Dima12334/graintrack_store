from datetime import datetime
from decimal import Decimal
from types import EllipsisType

from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.schemas.products.product_discount_schemas import (
    ProductDiscountCreateOutSchema,
    ProductDiscountUpdateSchema,
    ProductDiscountCreateInSchema,
)
from uuid import UUID

from graintrack_store.core.adapters.validators.base import BaseValidator
from graintrack_store.core.utils import remove_ellipsis_fields
from pydantic import ValidationError as PydanticValidationError


class ProductDiscountValidator(BaseValidator):
    product_repository: ProductRepository

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def validate_create(
        self,
        product_uuid: UUID,
        discount_started_at: datetime,
        discount_ended_at: datetime,
        discount_percentage: Decimal,
        is_active: bool = True,
    ) -> ProductDiscountCreateOutSchema:
        data = {
            "product_uuid": product_uuid,
            "discount_started_at": discount_started_at,
            "discount_ended_at": discount_ended_at,
            "discount_percentage": discount_percentage,
            "is_active": is_active,
        }
        try:
            schema = ProductDiscountCreateInSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        product = self.product_repository.retrieve_by_uuid(
            instance_uuid=schema.product_uuid
        )
        if not product:
            raise ValidationError(f"Product with uuid {schema.product_uuid} not found.")

        out_data = schema.dict(exclude_unset=True)
        out_data["product_id"] = product.id

        return ProductDiscountCreateOutSchema(**out_data)

    def validate_update(
        self,
        discount_started_at: datetime | EllipsisType = ...,
        discount_ended_at: datetime | EllipsisType = ...,
        discount_percentage: Decimal | EllipsisType = ...,
        is_active: bool | EllipsisType = ...,
    ) -> ProductDiscountUpdateSchema:
        data = {
            "discount_started_at": discount_started_at,
            "discount_ended_at": discount_ended_at,
            "discount_percentage": discount_percentage,
            "is_active": is_active,
        }
        data = remove_ellipsis_fields(data)
        try:
            schema = ProductDiscountUpdateSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        return schema
