from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0)
    proposal_no: str = Field(max_length=30, nullable=False)
    commencement_date: date = Field(nullable=False, default=date.today())
    is_active: bool = Field(default=True)

    def __repr__(self):
        return f"<Proposal id({self.id}) user_id({self.user_id}) proposal_no({self.proposal_no})"