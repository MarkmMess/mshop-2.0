from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        table_name = cls.__name__.lower()
        if table_name[-1] == "y":
            return table_name.replace("y", "ies")
        return f"{table_name}s"

    id: Mapped[int] = mapped_column(primary_key=True)
