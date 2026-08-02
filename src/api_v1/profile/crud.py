from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.profile import Profile
from .schemas import CreateProfile, UpdateProfile
from api_v1.products.crud import get_products_by_user
from .errors import not_found


async def create_profile(
    data: CreateProfile,
    user_id: int,
    session: AsyncSession,
):
    profile = Profile(
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        mobile=data.mobile,
        user_id=user_id,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return await get_profile(profile.user_id, session)


async def get_profile(
    user_id: int,
    session: AsyncSession,
):
    profile = await session.get(Profile, user_id)
    if not profile:
        raise not_found()
    return profile


async def get_profile_with_products(
    user_id: int,
    session: AsyncSession,
):
    try:
        profile = await session.get(Profile, user_id)
        products = await get_products_by_user(session, user_id)
    except:
        raise not_found()

    return profile, products


async def update_profile(
    profile: UpdateProfile,
    partial: bool,
    user_id: int,
    session: AsyncSession,
):
    if not await session.get(Profile, user_id):
        raise not_found()
    for field, value in profile.model_dump(exclude_unset=partial).items():
        setattr(profile, field, value)
    await session.commit()
    return await get_profile(user_id, session)


async def delete_profile(
    user_id: int,
    session: AsyncSession,
):
    stmt = delete(Profile).where(Profile.user_id == user_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except:
        raise not_found()
    return "{message}: profile deleted successfully"
