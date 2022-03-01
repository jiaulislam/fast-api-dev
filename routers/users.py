from fastapi import APIRouter, status
from typing import List

from operations import user_operation
from schemas.user import User
from models.user import User as UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[User])
async def get_users():
    db_user = await user_operation.get_all_user()
    return db_user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel) -> User:
    _user: User = await user_operation.create_user(user)
    return _user


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    _user: User = await user_operation.get_user_by_id(user_id)
    return _user


