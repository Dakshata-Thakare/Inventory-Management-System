from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_password_hash
from database import get_db
from dependencies import get_current_user
from schemas import UserCreate,AdminCreate
from database_models import User
from permissions import require_role

router = APIRouter()


@router.get("/admin")
def admin_dashboard(current_user=Depends(require_role("admin"))):
    return {"message":"Welcome Admin"}

@router.post("/admin")
def create_admin(current_user=Depends(require_role("superadmin"))):
    pass

@router.get("/reports")
def reports(current_user=Depends(require_role("admin","superadmin"))):
    return "reports"

@router.post("/admins")
def create_admin(admin: AdminCreate,db:Session = Depends(get_db),current_user = Depends(require_role("superadmin"))):
    db_user = User(
        username=admin.username,
        email=admin.email,
        hashed_password=get_password_hash(admin.password),
        role="admin"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Admin Created"}
