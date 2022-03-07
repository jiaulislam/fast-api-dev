from datetime import timedelta, datetime
from sqlmodel import Session, select

import errors
from database import engine
from models import Users as UserModel
from schemas.user import TokenData, User as UserSchema
from typing import List, Optional
from fastapi import Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from utility import get_password_hash, verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

async def get_user_by_name(user_name: Optional[str]) -> UserModel:
    if user_name:
        with Session(engine) as session:
            statement = select(UserModel).where(UserModel.username == user_name)
            try:
                user = session.exec(statement).one()
                return user
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
                )
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


async def authenticate_user(username: str, password: str) -> UserSchema:
    if is_username_available(username):
        user = await get_user_by_name(username)
        if verify_password(password, user.password):
            return UserSchema(**user.dict())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.INVALID_CREDENTIALS
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
    )

def create_access_token(data: dict, expired_delta: Optional[timedelta]  = None):
    to_encode = data.copy()
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_name(token_data.username)
    return user
