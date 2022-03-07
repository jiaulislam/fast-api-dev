from sqlmodel import SQLModel, Session
from database import engine
from models import Users, Proposal, ProposerAttachments, ProposerNominee, NomineeAttachment


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db_and_tables()
    # create_users()
