from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session, select
from database import engine
from sqlalchemy.exc import NoResultFound, IntegrityError
from typing import List
import errors

from models import Proposal
from models import User


router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
)


@router.get("/", response_model=List[Proposal])
async def get_proposals():
    with Session(engine) as session:
        statement = select(Proposal)
        proposals = session.exec(statement).all()
        _proposals = [Proposal(**proposal.dict()) for proposal in proposals]
        return _proposals


@router.get("/{proposal_id}", response_model=Proposal)
async def get_proposal_by_id(proposal_id: int):
    with Session(engine) as session:
        statement = select(Proposal).where(Proposal.id == proposal_id)
        try:
            proposal = session.exec(statement).one()
            return Proposal(**proposal.dict())
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.RECORD_NOT_FOUND
            )


@router.post("/", response_model=Proposal)
async def create_proposal(proposal: Proposal):
    with Session(engine) as session:
        try:
            session.add(proposal)
            session.commit()
            session.refresh(proposal)
            return proposal
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.INVALID_REQUEST_BODY,
            )


@router.get("/user/{user_id}", response_model=List[Proposal])
async def get_proposals_by_user(user_id: int):
    with Session(engine) as session:
        statement = select(Proposal).where(Proposal.user_id == user_id)
        user_state = select(User).where(User.id == user_id)
        user = session.exec(user_state).one()
        print(user)
        proposals = session.exec(statement).all()
        _proposals = [Proposal(**proposal.dict()) for proposal in proposals]
        return _proposals
