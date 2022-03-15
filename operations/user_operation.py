from typing import Literal

from sqlalchemy.orm import Session
import errors
from models import User
from operations.sms import create_sms_row, get_sms_format
from schemas.user import ResetPassSchema, UserCreate
from fastapi import status, HTTPException
from utility import generate_random_password, get_hashed_password, verify_password
from schemas.sms import ActionChoices as choose


def is_username_available(db: Session, username: str) -> bool:
    _user: User|None = db.query(User).filter(User.username == username).first()
    if _user:
        return False
    return True

def is_email_available(db: Session, email: str) -> bool:
    _user: User|None = db.query(User).filter(User.email == email).first()
    if _user:
        return False
    return True

def is_mobile_available(db: Session, mobile: str) -> bool:
    _user: User|None = db.query(User).filter(User.mobile == mobile).first()
    if _user:
        return False
    return True

def authenticate_user(db: Session, username: str, password: str) -> User|Literal[False]:
    _user = db.query(User).filter(User.username == username).first()
    if not _user:
        return False
    if not verify_password(password, _user.password):
        return False
    return _user


def create_user(user: UserCreate, db: Session):
    if not is_username_available(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.USER_ALREADY_EXISTS)
    if not is_mobile_available(db, user.mobile):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.MOBILE_ALREADY_EXISTS)
    if user.email:
        if not is_email_available(db, user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors.EMAIL_ALREADY_EXISTS)
    db_user = User(**user.dict())
    random_pass = generate_random_password()
    create_sms_row(get_sms_format(user.username, random_pass, user.mobile), db)
    db_user.password = get_hashed_password(random_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def reset_password(user: ResetPassSchema, db: Session):
    if not is_username_available(db, user.username):
        _user: User = db.query(User).filter(User.username==user.username).one()
        if _user.mobile == user.mobile:
            random_pass = generate_random_password()
            create_sms_row(get_sms_format(user.username, random_pass, user.mobile, choose.FORGOT_PASSWORD), db)
            _user.password = get_hashed_password(random_pass)
            db.commit()
            db.refresh(_user)
            return _user
        else:
            raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, detail=errors.VALIDATION_ERROR)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors.USER_NOT_FOUND)


def change_password(user: User, new_password: str, db: Session):
    hashed_pass = get_hashed_password(new_password)
    user.password = hashed_pass
    db.commit()
    db.refresh(user)
    return user