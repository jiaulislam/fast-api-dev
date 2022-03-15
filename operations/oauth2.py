from datetime import timedelta, datetime
from typing import Any, Optional
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import errors
from sqlalchemy.orm import Session
from models import User
from schemas.user import UserBase
from services import get_db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception: Exception, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get('user_name')
        if not username:
            raise credential_exception
        try:
            _user = db.query(User).filter(User.username == username).one()
        except NoResultFound:
            raise credential_exception
        except MultipleResultsFound:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=errors.MULTIPLE_RESULT_FOUND)
    except JWTError:
        raise credential_exception
    return _user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=errors.VALIDATION_ERROR,
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, credential_exception, db)