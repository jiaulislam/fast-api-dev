# from sqlmodel import create_engine, Session

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIALECT = "oracle"
SQL_DRIVER = "cx_oracle"
USERNAME = "jibon"  # enter your username
PASSWORD = "jibon345"  # enter your password
HOST = "192.168.1.34"  # enter the oracle db host url
PORT = 1521  # enter the oracle port number
SERVICE = "PRAGATI"  # enter the oracle db service name
tns = (
    "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.34)(PORT = 1521))"
    "(CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = PRAGATI)))"
)


ENGINE_PATH_WIN_AUTH = (
    DIALECT + "+" + SQL_DRIVER + "://" + USERNAME + ":" + PASSWORD + "@" + tns
)


engine = create_engine(ENGINE_PATH_WIN_AUTH, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# engine = create_engine(ENGINE_PATH_WIN_AUTH, echo=True)
