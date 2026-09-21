from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from . import crud
from .schemas import CreateProfile, ProfileRead, UpdateProfile
from ..auth.schemas import UserRead
from ..auth.service import get_current_active_auth_user

router = APIRouter()


@router.post("/create", response_model=ProfileRead)
async def create_profile(
    profile: CreateProfile,
    user=Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProfileRead:
    return await crud.create_profile(profile, user.id, session)


@router.get("/profile", response_model=ProfileRead)
async def my_profile(
    user=Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProfileRead:
    return await crud.get_profile(user.id, session)


@router.get("/profile/{user_id}", response_model=ProfileRead | None)
async def profile_read(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProfileRead:
    return await crud.get_profile(user_id, session)


@router.get("/profile/products/{user_id}")
async def profile_product(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_profile_with_products(user_id, session)


@router.put("/profile/update", response_model=ProfileRead)
async def profile_update(
    profile: UpdateProfile,
    user=Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_profile(
        profile_update=profile,
        partial=False,
        user_id=user.id,
        session=session,
    )


@router.patch("/profile/update/partial", response_model=ProfileRead)
async def profile_update_partial(
    profile: UpdateProfile,
    user=Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProfileRead:
    return await crud.update_profile(
        profile=profile,
        partial=True,
        user_id=user.id,
        session=session,
    )


@router.delete("/delete")
async def delete_profile(
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_profile(user.id, session)
