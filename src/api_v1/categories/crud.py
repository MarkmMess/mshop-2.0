from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Category


async def create_category(session: AsyncSession, name) -> Category:
    category = Category(name=name)
    session.add(category)
    await session.flush()
    return category


async def get_category(session: AsyncSession, name: str) -> Category | None:
    stmt = select(Category.name).where(Category.name == name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
