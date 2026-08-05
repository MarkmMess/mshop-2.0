from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String, Numeric, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column


from .base import Base
from .user import User


if TYPE_CHECKING:
    from .user import User


class Product(Base):
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    category: Mapped[str] = mapped_column(
        ForeignKey("categories.name"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="products")
