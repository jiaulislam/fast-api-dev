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
    _user = user_operation.create_user(user, db)
    return _user

