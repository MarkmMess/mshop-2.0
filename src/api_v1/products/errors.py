from fastapi import HTTPException, status


def forbidden(detail: str = "Forbidden"):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def not_found(detail: str = "Product not found"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )


def unprocessable_entity(detail: str = "Quantity must be greater than 0"):
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
    )
