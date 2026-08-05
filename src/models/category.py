from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Relationship, Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    product: Mapped[list["Product"]] = Relationship(back_populates="category")
