from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .profile import Profile
    from .product import Product


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)
    active: Mapped[bool] = mapped_column(nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="user")
    products: Mapped[list["Product"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id:{self.id}, username:{self.username!r})"

    def ___repr__(self):
        return str(self)
