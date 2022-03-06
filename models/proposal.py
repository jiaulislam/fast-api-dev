from sqlmodel import Relationship, SQLModel, Field
from datetime import date, datetime
from typing import Optional


class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id")
    proposal_no: str = Field(max_length=30, nullable=False)
    commencement_date: date = Field(nullable=False, default=date.today())
    users: "Users" = Relationship(back_populates="proposals")
    created_at: Optional[datetime]

    def __repr__(self):
        return f"<Proposal id({self.id}) user_id({self.user_id}) proposal_no({self.proposal_no})"
