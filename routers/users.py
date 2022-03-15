from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from operations import user_operation
from models import User
from operations.oauth2 import get_current_user
from schemas.user import UserBase, UserCreate, UserOut
from services import get_db
from typing import List
import errors

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    _user = user_operation.create_user(user, db)
    return _user


@router.get("/", response_model=List[UserBase])
async def get_all_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserBase)
async def get_a_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_admin:
        _user = db.query(User).filter(User.id == user_id).first()
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
            )
        return _user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail=errors.NOT_AUTHORIZED
    )


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_user_by_id(
    user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=errors.NOT_AUTHORIZED
        )

    _user = db.query(User).filter(User.id == user_id).first()
    db.delete(_user)
    db.commit()
