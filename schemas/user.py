from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    full_name: str
    mobile: Optional[str]
    email: Optional[str]
    is_active: bool
    is_admin: bool
    is_agent: bool
    # created_at: Optional[datetime]

class LoginSchema(BaseModel):
    email: str
    password: str

class UserStatusSchema(BaseModel):
    username: str
    available: bool