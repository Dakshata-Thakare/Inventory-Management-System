from typing import Annotated
from database import get_db
import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from auth import (
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
    get_user
)

from schemas import User, TokenData


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],db: Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",)
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username,role=role)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(
        db,
        token_data.username
    )

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: Annotated[User,Depends(get_current_user)]):
    print("current_user: ",current_user.username)
    print("current_user is active: ",current_user.is_active)
    # print("current_user password: ",current_user.password)

    if not(current_user.is_active):
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user