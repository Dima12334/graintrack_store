from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.schemas.products.product_income_schemas import (
    ProductIncomeCreateOutSchema,
    ProductIncomeCreateInSchema,
)
from uuid import UUID

from graintrack_store.core.adapters.validators.base import (
    BaseValidator,
    ProductValidationMixin,
)
from pydantic import ValidationError as PydanticValidationError


class ProductIncomeValidator(ProductValidationMixin, BaseValidator):

    product_repository: ProductRepository

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def validate_create_product_income(
        self, product_uuid: UUID, quantity: int
    ) -> ProductIncomeCreateOutSchema:
        data = {"product_uuid": product_uuid, "quantity": quantity}
        try:
            schema = ProductIncomeCreateInSchema(**data)
        except PydanticValidationError as ex:
            errors = self.parse_pydantic_validation_error(ex)
            raise ValidationError(errors)

        product = self.validate_product(product_uuid=schema.product_uuid)

        out_data = schema.dict(exclude_unset=True)
        out_data["product_id"] = product.id

        return ProductIncomeCreateOutSchema(**out_data)
