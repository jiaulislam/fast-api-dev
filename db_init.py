from sqlmodel import SQLModel, Session
from database import engine
from models.user import Users
from models.proposal import Proposal


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db_and_tables()
    # create_users()
