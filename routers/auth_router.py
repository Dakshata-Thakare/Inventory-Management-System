from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token,User,UserInDB,UserResponse
from auth import authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import fake_users_db,get_current_active_user

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()]) -> Token:
    # print("username: ",form_data.username)
    # print("password: ",form_data.password)
    user = authenticate_user(fake_users_db,form_data.username,form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/users/me",response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User,Depends(get_current_active_user)]):
    return current_user