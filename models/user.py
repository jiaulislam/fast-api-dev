from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, min_length=3, max_length=50)
    email: Optional[str] = Field(max_length=50, nullable=True)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime]

    def __repr__(self):
        return f"<User id({self.id} name({self.name}))>"
