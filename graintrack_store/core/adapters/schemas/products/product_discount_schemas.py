from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from graintrack_store.core.constants import DECIMAL_MAX_DIGITS_FOR_PERCENT, DECIMAL_PLACES_FOR_PERCENT


class ProductDiscountCreateInSchema(BaseModel):
    product_uuid: UUID
    discount_started_at: datetime
    discount_ended_at: datetime
    discount_percentage: Decimal = Field(
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
        gt=Decimal(0)
    )
    is_active: bool = Field(default=True)


class ProductDiscountCreateOutSchema(BaseModel):
    product_id: int
    discount_started_at: datetime
    discount_ended_at: datetime
    discount_percentage: Decimal = Field(
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
        gt=Decimal(0)
    )
    is_active: bool = Field(default=True)


class ProductDiscountUpdateSchema(BaseModel):
    discount_started_at: Optional[datetime]
    discount_ended_at: Optional[datetime]
    discount_percentage: Optional[Decimal] = Field(
        max_digits=DECIMAL_MAX_DIGITS_FOR_PERCENT,
        decimal_places=DECIMAL_PLACES_FOR_PERCENT,
        gt=Decimal(0)
    )
    is_active: Optional[bool]
