from fastapi import APIRouter

from .products.views import router as product_router
from .auth.views import router as auth_router
from .profile.views import router as profile_router

router = APIRouter()
router.include_router(router=product_router, prefix="/products", tags=["products"])

router.include_router(
    router=auth_router,
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    router=profile_router,
    prefix="/profile",
    tags=["profile"],
)
