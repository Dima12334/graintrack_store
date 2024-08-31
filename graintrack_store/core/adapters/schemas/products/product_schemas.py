from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from graintrack_store.core.constants import DECIMAL_MAX_DIGITS_FOR_PERCENT, DECIMAL_PLACES_FOR_PERCENT, \
    DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from graintrack_store.products.constants import ProductConstants


class ProductCreateInSchema(BaseModel):
    category_uuid: UUID
    is_deleted: bool = Field(default=False)
    name: str = Field(max_length=ProductConstants.NAME_MAX_LENGTH)
    price: Decimal = Field(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, gt=Decimal(0))
    description: str = Field(max_length=ProductConstants.DESCRIPTION_MAX_LENGTH, default="")
    available_quantity: int = Field(default=0)


class ProductCreateOutSchema(BaseModel):
    category_id: int
    is_deleted: bool = Field(default=False)
    name: str = Field(max_length=ProductConstants.NAME_MAX_LENGTH)
    price: Decimal = Field(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, gt=Decimal(0))
    description: str = Field(max_length=ProductConstants.DESCRIPTION_MAX_LENGTH, default="")
    available_quantity: int = Field(ge=0, default=0)


class ProductUpdateInSchema(BaseModel):
    category_uuid: Optional[UUID]
    is_deleted: Optional[bool]
    name: Optional[str] = Field(max_length=ProductConstants.NAME_MAX_LENGTH)
    price: Optional[Decimal] = Field(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, gt=Decimal(0))
    description: Optional[str] = Field(max_length=ProductConstants.DESCRIPTION_MAX_LENGTH)


class ProductUpdateOutSchema(BaseModel):
    category_id: Optional[int]
    is_deleted: Optional[bool]
    name: Optional[str] = Field(max_length=ProductConstants.NAME_MAX_LENGTH)
    price: Optional[Decimal] = Field(max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, gt=Decimal(0))
    description: Optional[str] = Field(max_length=ProductConstants.DESCRIPTION_MAX_LENGTH)
