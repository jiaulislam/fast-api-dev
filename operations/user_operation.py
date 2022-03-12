from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from services import ALGORITHM, get_db, oauth2_scheme, SECRET_KEY
import errors
from database import engine
from models import User
from schemas.user import TokenData, UserCreate
from typing import List, Optional
from fastapi import Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from utility import get_password_hash, verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



# async def get_all_user() -> List[UserSchema]:
#     with Session(engine) as session:
#         statement = select(UserModel)
#         users = session.exec(statement).all()
#         _users = [UserSchema(**user.dict()) for user in users]
#         return _users


# async def get_user_by_id(user_id: int) -> UserSchema:
#     with Session(engine) as session:
#         statement = select(UserModel).where(UserModel.id == user_id)
#         try:
#             user = session.exec(statement).one()
#             return UserSchema(**user.dict())
#         except NoResultFound:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
#             )

def get_user_by_name(user_name: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == user_name).first()
        
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = errors.INVALID_CREDENTIALS,
        headers = {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub', None)
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    # user = get_user_by_name(token_data.username, db)
# async def is_username_available(username: str) -> bool:
#     with Session(engine) as session:
#         statement = select(UserModel).where(UserModel.username == username)
#         _usernames = session.exec(statement).all()
#         if _usernames:
#             return False
#         return True


def create_user(user: UserCreate, db: Session) -> User:
    db_user = User(**user.dict())
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# async def authenticate_user(username: str, password: str) -> UserSchema:
#     if is_username_available(username):
#         user = await get_user_by_name(username)
#         if verify_password(password, user.password):
#             return UserSchema(**user.dict())
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail=errors.INVALID_CREDENTIALS
#         )
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND
#     )

# def create_access_token(data: dict, expired_delta: Optional[timedelta]  = None):
#     to_encode = data.copy()
#     if expired_delta:
#         expire = datetime.utcnow() + expired_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub", None)
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = await get_user_by_name(token_data.username)
#     return user
