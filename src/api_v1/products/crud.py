from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from .dependencies import check_quantity, check_create_product_permission
from .errors import not_found
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial, ProductRet
from models.product import Product
from ..categories.service import check_category


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
    result = await session.get(Product, product_id)
    return result


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
    await session.delete(product)
    await session.commit()
