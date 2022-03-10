from database import engine, Base
from models import *

def create_db_and_tables():
    Base.metadata.create_all(bind=engine) # type: ignore


if __name__ == "__main__":
    create_db_and_tables()