from typing import Optional

from pydantic import BaseModel

from database import USERNAME

class UserCreate(BaseModel):
    id: Optional[int]
    username: str
    full_name: str
    mobile: str
    email: Optional[str]
    is_active: bool = True
    is_employee: bool = False
    is_admin: bool = False
    is_agent: bool = False
    emp_code: Optional[str]
    agent_code : Optional[str]

class UserBase(BaseModel):
    id: int
    username: str
    full_name: str
    mobile: Optional[str]
    email: Optional[str]
    is_active: bool = True
    is_employee: bool = False
    is_admin: bool = False
    is_agent: bool = False
    emp_code: Optional[str]
    agent_code : Optional[str]

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: str
    password: str


class UserStatusSchema(BaseModel):
    username: str
    available: bool

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    mobile: Optional[str]
    email: Optional[str]

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ResetPassSchema(BaseModel):
    username: str
    mobile: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str