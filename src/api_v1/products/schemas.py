from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field



class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(gt=0, decimal_places=2, max_digits=10)
    category_name: Optional[str] = Field(None, max_length=50)
    quantity: Optional[int]


class ProductCreate(ProductBase):
    quantity: Optional[int] = 1
    model_config = ConfigDict(extra="forbid")
    pass


class ProductUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(gt=0, decimal_places=2, max_digits=10)
    quantity_name: Optional[int] = Field(gt=0, max_digits=1000)
    category: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(extra="forbid")


class ProductUpdatePartial(ProductUpdate):
    pass


class ProductsRet(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    id: int
    user_id: int
    quantity: Optional[int] = Field(gt=0)
    category_name: Optional[str] = Field(None, max_length=50)
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: lambda v: float(v) if v else 0,
            datetime: lambda v: v.isoformat(),
        },
    )


class ProductRet(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    id: int
    user_id: int
    quantity: Optional[int]
    category_name: Optional[str] = Field(None, max_length=50)
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: lambda v: float(v) if v else 0,
            datetime: lambda v: v.isoformat(),
        },
    )
