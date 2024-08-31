from uuid import UUID
from pydantic import BaseModel, Field


class ProductIncomeCreateInSchema(BaseModel):
    product_uuid: UUID
    quantity: int = Field(gt=0)


class ProductIncomeCreateOutSchema(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
