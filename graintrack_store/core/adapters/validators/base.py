from typing import List
from uuid import UUID

from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError

from graintrack_store.products.models import Product, ProductCategory


class BaseValidator:

    def parse_pydantic_validation_error(
        self, exception: PydanticValidationError
    ) -> List[str]:
        errors = []
        for error in exception.errors():
            field = ".".join([str(el) for el in error["loc"]])
            message = error["msg"]
            errors.append(f"{field}: {message}")

        return errors


class ProductCategoryValidationMixin:

    def validate_category(self, category_uuid: UUID) -> ProductCategory:
        category = self.product_category_repository.retrieve_by_uuid(
            instance_uuid=category_uuid
        )
        if not category:
            raise ValidationError(
                f"Product category with uuid {category_uuid} not found."
            )
        return category


class ProductValidationMixin:

    def validate_product(self, product_uuid: UUID) -> Product:
        product = self.product_repository.retrieve_by_uuid(instance_uuid=product_uuid)
        if not product:
            raise ValidationError(f"Product with uuid {product_uuid} not found.")
        return product
