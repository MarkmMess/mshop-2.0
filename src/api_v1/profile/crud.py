from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User
from models.profile import Profile
from .schemas import CreateProfile, UpdateProfile
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
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.profile),
            selectinload(User.products),
        )
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise not_found()

    return user.profile, user.products


async def update_profile(
    profile_update: UpdateProfile,
    partial: bool,
    user_id: int,
    session: AsyncSession,
) -> type[Profile | None]:
    profile = await session.get(Profile, user_id)
    if not profile:
        raise not_found()
    for field, value in profile_update.model_dump(exclude_unset=partial).items():
        setattr(profile, field, value)
    await session.commit()
    await session.refresh(profile)
    return profile


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
