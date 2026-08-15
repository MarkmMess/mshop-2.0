from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Category
from .crud import get_category, create_category


async def check_category(session: AsyncSession, name: str) -> Category | None:
    is_exist = await get_category(session, name)
    if is_exist is None:
        await create_category(session, name)
        return await get_category(session, name)
    return is_exist
