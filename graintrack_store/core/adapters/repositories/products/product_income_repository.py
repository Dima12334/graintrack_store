from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.products.models import ProductIncome


class ProductIncomeRepository(BaseRepository):
    model = ProductIncome
