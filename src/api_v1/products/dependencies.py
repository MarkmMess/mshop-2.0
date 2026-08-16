from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from .errors import not_found
from .schemas import ProductRet
from . import crud
from models import db_helper


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProductRet:
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return ProductRet.model_validate(product)
    raise not_found()


def paginate(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=20, le=100, description="Number of items per page"),
) -> Params:
    return Params(page=page, size=size)
