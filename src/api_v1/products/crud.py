from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from .errors import not_found
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial, ProductRet
from models.product import Product


async def get_products(session: AsyncSession, params: Params) -> Page[ProductRet]:
    stmt = select(Product).order_by(Product.created_at.desc())
    return await apaginate(session, stmt, params=params)


async def get_products_by_user(session: AsyncSession, user_id: int) -> list[ProductRet]:
    stmt = (
        select(Product)
        .order_by(Product.created_at.desc())
        .where(Product.user_id == user_id)
    )
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    if not products:
        raise not_found()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(
    session: AsyncSession,
    product_data: ProductCreate,
    user_id: int,
) -> Product | None:
    product_dict = product_data.model_dump()
    product_dict["user_id"] = user_id
    product = Product(**product_dict)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    ret = await get_product(session, product.id)
    return ret


async def update_product(
    session: AsyncSession,
    product: ProductRet,
    product_update: ProductUpdate | ProductUpdatePartial,
    category: str | None = None,
    partial: bool = False,
) -> ProductRet:
    product_dict = product.model_dump()
    product_dict["category"] = category
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: ProductRet) -> None:
    await session.delete(product)
    await session.commit()
