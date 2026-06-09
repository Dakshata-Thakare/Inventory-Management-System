from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_password_hash
from database import get_db
from schemas import UserCreate
from database_models import User

router = APIRouter()

@router.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()

    return {
        "message": "User Created"
    }