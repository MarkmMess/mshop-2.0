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

def unprocessable_entity():
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Quantity must be greater than 0",
    )
