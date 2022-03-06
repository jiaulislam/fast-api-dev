from sqlmodel import Session, select

import errors
from database import engine
from models import Users as UserModel
from schemas.user import User as UserSchema
from typing import List
from fastapi import status, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from utility import get_password_hash


async def get_all_user() -> List[UserSchema]:
    with Session(engine) as session:
        statement = select(UserModel)
        users = session.exec(statement).all()
        _users = [UserSchema(**user.dict()) for user in users]
        return _users


async def get_user_by_id(user_id: int) -> UserSchema:
    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.id == user_id)
        try:
            user = session.exec(statement).one()
            return UserSchema(**user.dict())
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
            )


async def is_username_available(username: str) -> bool:
    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.username == username)
        _usernames = session.exec(statement).all()
        if _usernames:
            return False
        return True


async def create_user(user: UserModel) -> UserModel:
    with Session(engine) as session:
        existing_user: bool = await is_username_available(user.username)
        if existing_user:
            user.password = get_password_hash(user.password)
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=errors.INVALID_REQUEST_BODY,
                )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=errors.USER_ALREADY_EXISTS
        )
