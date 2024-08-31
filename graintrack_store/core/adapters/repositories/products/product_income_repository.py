from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.products.models import ProductIncome


class ProductIncomeRepository(BaseRepository):
    model = ProductIncome

    def get_base_qs(self):
        return ProductIncome.objects.select_related("product").all()

    def create(
        self,
        product_id: int,
        quantity: int,
    ) -> ProductIncome:
        data = {
            "product_id": product_id,
            "quantity": quantity,
        }
        product_income = ProductIncome(**data)
        product_income.save()
        return product_income
