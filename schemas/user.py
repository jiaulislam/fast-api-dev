from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: Optional[str]
    is_active: bool
    # created_at: Optional[datetime]
