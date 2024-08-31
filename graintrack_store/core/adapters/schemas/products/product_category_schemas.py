from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from graintrack_store.products.constants import ProductCategoryConstants


class ProductCategoryCreateInSchema(BaseModel):
    parent_category_uuid: Optional[UUID]
    name: str = Field(max_length=ProductCategoryConstants.NAME_MAX_LENGTH)
    description: str = Field(max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH)


class ProductCategoryCreateOutSchema(BaseModel):
    parent_category_id: Optional[int]
    name: str = Field(max_length=ProductCategoryConstants.NAME_MAX_LENGTH)
    description: str = Field(max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH)


class ProductCategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(max_length=ProductCategoryConstants.NAME_MAX_LENGTH)
    description: Optional[str] = Field(max_length=ProductCategoryConstants.DESCRIPTION_MAX_LENGTH)
