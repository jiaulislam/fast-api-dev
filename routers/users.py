from fastapi import APIRouter, status
from typing import List

from operations import user_operation
from schemas.user import User, UserStatusSchema
from models import Users as UserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=List[User])
async def get_users():
    db_user = await user_operation.get_all_user()
    return db_user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel) -> User:
    _user: UserModel = await user_operation.create_user(user)
    return User(**_user.dict())


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    _user: User = await user_operation.get_user_by_id(user_id)
    return _user


@router.get("/check_username/{username}", response_model=UserStatusSchema)
async def check_username(username: str) -> UserStatusSchema:
    _status: bool = await user_operation.is_username_available(username)
    return UserStatusSchema(username=username, available=_status)
