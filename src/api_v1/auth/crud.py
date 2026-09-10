from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .security import hash_password
from models import (
    User,
    Product,
)
from .schemas import CreateUser, UserRead, UserValidation, UserUpdate, UserUpdatePartial
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


async def get_user(session: AsyncSession, user_id: int) -> UserRead | None:
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    return user


async def get_user_for_validation(
    session: AsyncSession, username: str
) -> UserValidation | None:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    return user


async def get_user_with_products(session: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    if user:
        ret = f"username: {user.username}"
        stmt = select(Product).where(Product.user_id == user.id)
        products: list[Product] | None = await session.scalar(stmt)
        if products:
            ret += "*" * 10
            ret += "Items for sale:"
            for product in products:
                ret += f"name: {product.name} price: {product.price}"
        return ret
    raise not_found


async def update_user(
    session: AsyncSession,
    user: UserRead,
    user_upd: UserUpdate | UserUpdatePartial,
) -> UserRead | None:
    for name, value in user_upd.model_dump().items():
        setattr(user, name, value)
    try:
        await session.commit()
        await session.refresh(user)
        return await get_user(session, user.id)
    except Exception:
        raise taken_name


async def del_user(session: AsyncSession, user):
    await session.delete(user)
    await session.commit()
    return "message: User deleted"
