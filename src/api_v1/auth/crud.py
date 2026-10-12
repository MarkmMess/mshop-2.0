from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload

from .security import hash_password
from models import User
from .schemas import CreateUser, UserRead, UserValidation, UserUpdate
from .errors import not_found, taken_name


async def create_user(session: AsyncSession, user_info: CreateUser) -> UserRead:
    check = await get_user_for_validation(session, user_info.username)
    if check:
        raise taken_name
    hashed_password = hash_password(user_info.password)
    user = User(
        username=user_info.username,
        email=user_info.email,
        active=True,
        hashed_password=hashed_password,
    )
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise taken_name
    return UserRead.model_validate(user)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    return user


async def get_user_for_validation(
    session: AsyncSession, username: str
) -> UserValidation | None:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    return user


# async def get_user_with_products(session: AsyncSession, username: str):
#     stmt = (
#         select(User)
#         .where(User.username == username)
#         .options(selectinload(User.products))
#     )
#     user_with_products = await session.scalar(stmt)
#     if not user_with_products:
#         raise not_found
#     return user_with_products


async def update_user(
    session: AsyncSession,
    user: UserRead,
    user_upd: UserUpdate,
) -> UserRead | None:
    for name, value in user_upd.model_dump().items():
        setattr(user, name, value)
    try:
        await session.commit()
        await session.refresh(user)
        return user
    except Exception:
        raise taken_name


async def del_user(session: AsyncSession, user: UserRead) -> None:
    await session.delete(user)
    await session.commit()
