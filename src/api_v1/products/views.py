from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from .errors import forbidden
from ..auth.schemas import UserRead
from ..auth.service import get_current_active_auth_user
from ..categories.service import check_category
from . import crud
from .schemas import (
    ProductRet,
    ProductsRet,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from .dependencies import product_by_id, paginate


router = APIRouter()


def check_product_permission(product: ProductRet, user: UserRead):
    if product.user_id != user.id:
        raise forbidden


@router.post("/", response_model=ProductRet)
async def create_product(
    product: ProductCreate,
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await check_category(session, product.category_name)
    return await crud.create_product(
        product_data=product,
        user_id=user.id,
        session=session,
    )


@router.get("/", response_model=Page[ProductRet])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    params: Params = Depends(paginate),
):
    return await crud.get_products(session, params)


@router.get("/{product_id}", response_model=ProductRet)
async def get_product(product: ProductRet = Depends(product_by_id)):
    return product


@router.get("/users/{user_id}", response_model=list[ProductRet])
async def get_user_products(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products_by_user(session, user_id)


@router.put("/{product_id}", response_model=ProductRet)
async def update_full_product(
    product_update: ProductUpdate,
    user: UserRead = Depends(get_current_active_auth_user),
    product: ProductRet = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await check_category(session, product.category)
    check_product_permission(product, user)
    return await crud.update_product(
        product=product,
        product_update=product_update,
        session=session,
    )


@router.patch("/{product_id}", response_model=ProductRet)
async def product_update_partial(
    product_update: ProductUpdatePartial,
    product: ProductRet = Depends(product_by_id),
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    check_product_permission(product, user)
    return await crud.update_product(
        product=product,
        product_update=product_update,
        session=session,
        partial=True,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: ProductRet = Depends(product_by_id),
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    check_product_permission(product, user)
    await crud.delete_product(product=product, session=session)
