from rest_framework.exceptions import ValidationError

from graintrack_store.core.adapters.repositories.products.product_repository import ProductRepository
from graintrack_store.core.adapters.schemas.products.product_income_schemas import ProductIncomeCreateOutSchema, \
    ProductIncomeCreateInSchema
from uuid import UUID


class ProductIncomeValidator:

    product_repository: ProductRepository

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def validate_create(
        self,
        product_uuid: UUID,
        quantity: int
    ) -> ProductIncomeCreateOutSchema:
        data = {
            "product_uuid": product_uuid,
            "quantity": quantity
        }
        schema = ProductIncomeCreateInSchema(**data)

        product = self.product_repository.retrieve_by_uuid(instance_uuid=schema.product_uuid)
        if not product:
            raise ValidationError(f"Product with uuid {schema.product_uuid} not found.")

        out_data = schema.dict(exclude_unset=True)
        out_data["product_id"] = product.id

        return ProductIncomeCreateOutSchema(**out_data)
