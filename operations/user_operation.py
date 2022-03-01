from sqlmodel import Session, select

import errors
from database import engine
from models.user import User as UserModel
from schemas.user import User as UserSchema
from typing import List
from fastapi import status, HTTPException
from sqlalchemy.exc import NoResultFound,IntegrityError


async def get_all_user() -> List[UserSchema]:
    with Session(engine) as session:
        statement = select(UserModel)
        results = session.exec(statement)
        return results.all()


async def get_user_by_id(user_id: int) -> UserSchema:
    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.id == user_id)
        try:
            result = session.exec(statement).one()
            return result
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_ID_NOT_FOUND)


async def create_user(user: UserModel) -> UserSchema:
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return UserSchema(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active
            )
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.INVALID_REQUEST_BODY)