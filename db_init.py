from sqlmodel import SQLModel, Session
from database import engine
from models.user import User

# from models.proposal import Proposal


# def create_proposals():
#     proposal_1 = Proposal(user_id=1, proposal_no="13202938381")
#     proposal_2 = Proposal(user_id=2, proposal_no="32132123")
#     proposal_3 = Proposal(user_id=3, proposal_no="1354235202938381")
#
#     print(proposal_1)
#     print(proposal_2)
#     print(proposal_3)
#
#     with Session(engine) as session:
#         session.add(proposal_1)
#         session.add(proposal_2)
#         session.add(proposal_3)
#
#         session.commit()
#
#         print(proposal_1.proposal_no)
#


def create_users():
    user_1 = User(id=1, name="Jibon", email="jiaulislam.ict.bd@gmail.com")
    user_2 = User(id=2, name="Jamil", email="jamil.ict.bd@gmail.com")
    user_3 = User(id=3, name="Jhonny", email="jhonny.ict.bd@gmail.com")

    print(user_1)
    print(user_2)
    print(user_3)

    with Session(engine) as session:
        session.add(user_1)
        session.add(user_2)
        session.add(user_3)

        session.commit()

        print("After Commiting")
        print(user_1)
        print(user_2)
        print(user_3)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db_and_tables()
    # create_users()