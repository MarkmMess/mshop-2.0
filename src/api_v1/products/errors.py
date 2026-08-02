from fastapi import HTTPException, status

from models import product, user


def forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User {product.user_id} does not belong to {user.id}",
    )


def not_found():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )
