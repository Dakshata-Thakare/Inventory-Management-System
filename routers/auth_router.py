from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token,User,UserInDB,UserResponse
from auth import ALGORITHM, SECRET_KEY, authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,get_password_hash,create_refresh_token
from dependencies import fake_users_db,get_current_active_user
from database import get_db
from database_models import User as UserModel
from schemas import User,UserCreate
from sqlalchemy.orm import Session
import jwt

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    # form_data: Annotated[OAuth2PasswordRequestForm,Depends()]) -> Token:
    form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db: Session = Depends(get_db)):
    # print("username: ",form_data.username)
    # print("password: ",form_data.password)
    user = authenticate_user(db,form_data.username,form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(
        data={"sub": user.username,
              "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": user.username})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.get("/users/me",response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User,Depends(get_current_active_user)]):
    return current_user

@router.post("/register")
def register(user:UserCreate,db: Session = Depends(get_db)):
    existing_user = (db.query(UserModel).filter(UserModel.username == user.username).first())
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    existing_email = (db.query(UserModel).filter(UserModel.email == user.email).first())
    if existing_email:
        raise HTTPException(status_code=400,detail="Email already exists")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email = user.email,
        hashed_password = hashed_password
    )   #here how role is automatically added?

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message:User Created"}

#Currently refresh token exists only in JWT.
# Production systems store it:users table or refresh_tokens table.so logout can invalidate tokens.
# For now skiping that........
@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    payload = jwt.decode(refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401,detail="Invalid refresh token")
    username = payload.get("sub")
    user = get_user(db,username)
    new_access_token = create_access_token(data={"sub": username,"role": user.role})
    return {"access_token": new_access_token}