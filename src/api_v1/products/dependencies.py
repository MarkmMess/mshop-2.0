from typing import Annotated

from fastapi import Depends, Path, Query, HTTPException
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from .errors import not_found, unprocessable_entity, forbidden
from .schemas import ProductRet, ProductCreate
from . import crud
from models import db_helper, Product
from ..auth.schemas import UserRead
from ..profile.crud import get_profile
from ..categories.service import check_category


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return product
    raise not_found()


def paginate(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=20, le=100, description="Number of items per page"),
) -> Params:
    return Params(page=page, size=size)


def check_quantity(quantity: int):
    if quantity < 1:
        raise unprocessable_entity


def check_product_permission(product: ProductRet | Product, user: UserRead):
    if product.user_id != user.id:
        raise forbidden


async def check_create_product_permission(
        product_data: ProductCreate, 
        user_id: int,
        session: AsyncSession,
):
    try:
        await get_profile(user_id, session)
    except HTTPException as err:
        if err.status_code != 404:
            raise
        raise forbidden(
            detail="User profile not found. Please create a profile first."
        ) from None
    
    await check_category(session, product_data.category_name)
    check_quantity(product_data.quantity)
