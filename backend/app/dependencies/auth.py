from fastapi import Depends, HTTPException
from app.models import User
from app.services.auth_service import get_current_user


def require_admin(
        current_user: User = Depends(get_current_user)
        ):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Operation requires admin privileges"
            )
    return current_user

def require_owner_or_admin(
        resource_owner_id: int,
        current_user: User = Depends(get_current_user)
        ):
    if current_user.role != "admin" and current_user.id != resource_owner_id:
        raise HTTPException(
            status_code=403,
            detail="Operation requires owner or admin privileges"
            )
    return current_user


# TODO: require_premium_user
# TODO: require_verified_email
# TODO: require_wallet_owner