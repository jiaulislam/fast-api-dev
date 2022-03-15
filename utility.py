import string
import random
from passlib.context import CryptContext
from sqlalchemy import Column
from sqlalchemy.dialects.oracle import VARCHAR2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: Column[VARCHAR2]):
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_password(
    size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
):
    return "".join(random.choice(chars) for _ in range(size))
