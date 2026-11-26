from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.orm import selectinload

from models import Product, User
from .dependencies import check_quantity, check_create_product_permission
from .errors import not_found
from .schemas import (
    ProductCreate,
    ProductProfileRet,
    ProductUpdate,
    ProductUpdatePartial,
    ProductRet,
    SortOrder,
    sort_dict,
)
from ..categories.service import check_category


async def get_products(
    session: AsyncSession, params: Params, sort_by: str | None, order_by: SortOrder
) -> Page[ProductProfileRet]:
    if sort_by is None:
        stmt = (
            select(Product)
            .order_by(Product.created_at.desc())
            .options(selectinload(Product.user).selectinload(User.profile))
        )
    else:
        column = sort_dict[sort_by]
        stmt = (
            select(Product)
            .order_by(column.asc() if order_by == SortOrder.asc else column.desc())
            .options(selectinload(Product.user).selectinload(User.profile))
        )
    return await apaginate(
        conn=session, query=stmt, params=params  # pyright: ignore[reportArgumentType]
    )


async def get_products_by_user(
    session: AsyncSession, user_id: int, sort_by: str | None, order_by: SortOrder
) -> list[ProductProfileRet]:
    if sort_by is None:
        stmt = (
            select(Product)
            .order_by(Product.created_at.desc())
            .where(Product.user_id == user_id)
            .options(selectinload(Product.user).selectinload(User.profile))
        )
    else:
        column = sort_dict[sort_by]
        stmt = (
            select(Product)
            .order_by(column.asc() if order_by == SortOrder.asc else column.desc())
            .where(Product.user_id == user_id)
            .options(selectinload(Product.user).selectinload(User.profile))
        )
    result: Result[Product] = await session.execute(stmt)
    products = result.scalars().all()
    if not products:
        raise not_found()
    return [ProductProfileRet.model_validate(product) for product in products]


async def get_product(
    session: AsyncSession, product_id: int
) -> ProductProfileRet | None:
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.user).selectinload(User.profile))
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    return ProductProfileRet.model_validate(product) if product else None


async def create_product(
    session: AsyncSession,
    product_data: ProductCreate,
    user_id: int,
) -> ProductRet | None:
    await check_create_product_permission(product_data, user_id, session)

    product_dict = product_data.model_dump()
    product_dict["user_id"] = user_id
    product = Product(**product_dict)

    session.add(product)
    await session.commit()
    await session.refresh(product)

    return ProductRet.model_validate(product) if product else None


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    check_quantity(product_update.quantity)
    await check_category(session, str(product_update.category_name))

    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: ProductRet) -> None:
    db_product = await session.get(Product, product.id)
    if db_product is None:
        raise not_found()
    await session.delete(db_product)
    await session.commit()
