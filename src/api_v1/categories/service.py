from sqlalchemy.ext.asyncio import AsyncSession

from models import Category
from .crud import get_category, create_category


async def check_category(session: AsyncSession, name: str | None) -> Category | str:
    if not name:
        name = "Other"
    category = await get_category(session, name)
    if category is None:
        category = await create_category(session, name)
    return category
