from datetime import timedelta, datetime
from xmlrpc.client import boolean

from sqlalchemy.orm import Session
from sqlalchemy import select
import errors
from models import User
from schemas.user import TokenData, UserCreate
from fastapi import status, HTTPException
from utility import get_password_hash, verify_password


def get_user_by_name(user_name: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == user_name).first()
        


def is_username_available(db: Session, username: str) -> boolean:
    _user = db.query(User).filter(User.username == username).first()
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.USER_ALREADY_EXISTS)
    return False

def is_email_available(db: Session, email: str) -> boolean:
    _user = db.query(User).filter(User.email == email).first()
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQEUST, detail=errors.EMAIL_ALREADY_EXISTS)
    return False

def is_mobile_available(db: Session, mobile: str) -> boolean:
    _user = db.query(User).filter(User.mobile == mobile).first()
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.MOBILE_ALREADY_EXISTS)
    return False

def is_unique_user(db:Session, user: UserCreate):
    if not is_username_available(db, user.username) and not is_email_available(db, user.email) and not is_mobile_available(db, user.mobile):
        return True
    return False

def create_user(user: UserCreate, db: Session) -> User:
    if is_unique_user(db, user):
        db_user = User(**user.dict())
        db_user.password = get_password_hash(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
