from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import errors

from operations import user_operation
from models import User
from schemas.user import UserCreate, UserOut
from services import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    is_username_used = db.query(User).filter(User.username == user.username).first()
    is_mobile_used = db.query(User).filter(User.mobile == user.mobile).first()
    is_email_used = db.query(User).filter(User.email == user.email).first()
    if is_username_used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.USER_ALREADY_EXISTS)
    if is_mobile_used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.MOBILE_ALREADY_EXISTS)
    if is_email_used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.EMAIL_ALREADY_EXISTS)
    _user = user_operation.create_user(user, db)
    return _user

