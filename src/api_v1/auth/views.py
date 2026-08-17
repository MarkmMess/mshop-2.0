from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from .schemas import (
    TokenInfo,
    CreateUser,
    UserRead,
    UserValidation,
    UserUpdate,
    UserUpdatePartial,
)
from .service import (
    validate_auth_user,
    get_current_active_auth_user,
)
from . import crud
from . import security as auth_security


router = APIRouter()


@router.post("/signIn", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRead:
    return await crud.create_user(session, user)


@router.post("/login/new/", response_model=TokenInfo)
async def auth_user_jwt(
    user: UserValidation = Depends(validate_auth_user),
):
    jwt_token = {
        # subject
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_security.encode_jwt(jwt_token)
    return TokenInfo(
        access_token=token,
        token_type="bearer",
    )


@router.get("/check/user/")
def auth_user_check_info(
    user: UserRead = Depends(get_current_active_auth_user),
) -> UserRead:
    return user


@router.put("/update_user/", response_model=UserRead)
async def update_user(
    update_user_scheme: UserUpdate,
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(session, user, update_user_scheme)


@router.patch("/update_user_partial/", response_model=UserRead)
async def update_user_partial(
    update_user_scheme: UserUpdatePartial,
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_upd=update_user_scheme,
        partial=True,
    )


@router.delete("/delete_user/")
async def delete_user(
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.del_user(session, user)
