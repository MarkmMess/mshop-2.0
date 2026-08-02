from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(gt=0, decimal_places=2, max_digits=10)


class ProductCreate(ProductBase):
    model_config = ConfigDict(extra="forbid")
    pass


class ProductUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(gt=0, decimal_places=2, max_digits=10)

    model_config = ConfigDict(extra="forbid")


class ProductUpdatePartial(ProductUpdate):
    pass


class ProductRet(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: lambda v: float(v) if v else 0,
            datetime: lambda v: v.isoformat(),
        },
    )
