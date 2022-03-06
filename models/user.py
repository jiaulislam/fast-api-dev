from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from datetime import datetime
from models.proposal import Proposal
from typing import List


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        nullable=False, min_length=3, max_length=16, regex="^[a-zA-Z0-9_]*$"
    )
    full_name: str = Field(nullable=False, min_length=3, max_length=50)
    mobile: Optional[str] = Field(
        nullable=True,
        min_length=11,
        max_length=11,
        regex="^017|016|013|018|019|[0-9]{8}$",
    )
    email: Optional[str] = Field(max_length=50, nullable=True)
    password: str = Field(nullable=False, min_length=6, max_length=65)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_agent: bool = Field(default=True, nullable=False)
    proposals: List["Proposal"] = Relationship(back_populates="users")
    created_at: Optional[datetime]

    def __repr__(self):
        return f"<User id({self.id} name({self.username}))>"
