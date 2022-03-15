from datetime import timedelta
from fastapi import HTTPException, status, Depends
import errors
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User
from schemas.user import TokenData
from utility import verify_password
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
