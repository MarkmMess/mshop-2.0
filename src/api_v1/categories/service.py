from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Category
from .crud import get_category, create_category


async def check_category(session: AsyncSession, name: str) -> Category | None:
    if not name:
        name = 'Other'
    category = await get_category(session, name)
    if category is None:
        category = await create_category(session, name)
    return category
