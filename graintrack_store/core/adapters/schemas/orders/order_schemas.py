from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from graintrack_store.core.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from graintrack_store.orders.constants import OrderConstants


class OrderCreateSchema(BaseModel):
    status: str = Field(max_length=OrderConstants.STATUS_MAX_LENGTH)
    order_code: str = Field(max_length=OrderConstants.ORDER_CODE_MAX_LENGTH)
    comment: str = Field(max_length=OrderConstants.COMMENT_MAX_LENGTH, default="")
    total_sum: Decimal = Field(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        ge=Decimal(0),
        default=Decimal(0)
    )


class OrderUpdateSchema(BaseModel):
    status: Optional[str] = Field(max_length=OrderConstants.STATUS_MAX_LENGTH)
    comment: Optional[str] = Field(max_length=OrderConstants.COMMENT_MAX_LENGTH)
