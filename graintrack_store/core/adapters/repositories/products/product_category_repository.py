from types import EllipsisType
from typing import Optional

from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.core.utils import remove_ellipsis_fields
from graintrack_store.products.models import ProductCategory


class ProductCategoryRepository(BaseRepository):
    model = ProductCategory

    def create(
        self,
        name: str,
        description: str = "",
        parent_category_id: Optional[int] = None,
    ) -> ProductCategory:
        data = {
            "name": name,
            "description": description,
            "parent_category_id": parent_category_id,
        }
        product_category = ProductCategory(**data)
        product_category.save()
        return product_category

    def update(
        self,
        instance: ProductCategory,
        name: str | EllipsisType = ...,
        description: str | EllipsisType = ...,
    ) -> ProductCategory:
        data = {
            "name": name,
            "description": description,
        }
        data = remove_ellipsis_fields(data)

        for field, value in data:
            setattr(instance, field, value)

        instance.save()
        return instance
