from typing import Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    id: Optional[int]
    username: str
    full_name: str
    password: str
    mobile: Optional[str]
    email: Optional[str]
    is_active: bool
    is_admin: bool
    is_agent: bool
    emp_code: Optional[str]
    agent_code : Optional[str]


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