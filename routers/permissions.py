from fastapi import Depends,HTTPException,status
from dependencies import get_current_user


def require_role(*allowed_roles):
    async def role_checker(current_user = Depends(get_current_user)):

        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")
        return current_user

    return role_checker