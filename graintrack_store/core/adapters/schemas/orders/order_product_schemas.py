from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from graintrack_store.core.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES


class OrderProductCreateInSchema(BaseModel):
    order_uuid: UUID
    product_uuid: UUID
    quantity: int = Field(gt=0)


class OrderProductCreateOutSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(gt=0)
    price: Decimal = Field(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, gt=Decimal(0)
    )
    discount: Decimal = Field(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        ge=Decimal(0),
        default=Decimal(0),
    )


class OrderProductUpdateSchema(BaseModel):
    quantity: Optional[int] = Field(gt=0)
