from uuid import UUID

from django.db import transaction

from graintrack_store.core.adapters.repositories.products.product_income_repository import (
    ProductIncomeRepository,
)
from graintrack_store.core.adapters.repositories.products.product_repository import (
    ProductRepository,
)
from graintrack_store.core.adapters.services.base import BaseService
from graintrack_store.core.adapters.validators.products.product_income_validator import (
    ProductIncomeValidator,
)
from graintrack_store.products.models import ProductIncome


class ProductIncomeService(BaseService):
    product_income_repository: ProductIncomeRepository
    product_repository: ProductRepository
    product_income_validator: ProductIncomeValidator

    def __init__(self):
        self.product_income_repository = ProductIncomeRepository()
        self.repository = self.product_income_repository

        self.product_repository = ProductRepository()
        self.product_income_validator = ProductIncomeValidator(
            product_repository=self.product_repository
        )

    def create_product_income(self, product_uuid: UUID, quantity: int) -> ProductIncome:
        with transaction.atomic():
            validated_data = self.product_income_validator.validate_create(
                product_uuid=product_uuid,
                quantity=quantity,
            )
            product_income = self.product_income_repository.create(
                **validated_data.dict(exclude_unset=True)
            )

            self.product_repository.increase_available_quantity(
                product_id=product_income.product_id, quantity=product_income.quantity
            )
        return product_income
