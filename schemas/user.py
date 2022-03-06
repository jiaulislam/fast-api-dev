from typing import Optional

from pydantic import BaseModel

from models import Proposal


class User(BaseModel):
    id: int
    username: str
    full_name: str
    mobile: Optional[str]
    email: Optional[str]
    is_active: bool
    is_admin: bool
    is_agent: bool


class LoginSchema(BaseModel):
    email: str
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


class UserProposalSchemaOut(BaseModel):
    proposal: Proposal
    user: UserOut