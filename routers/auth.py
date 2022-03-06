from sqlmodel import Session, select
from database import engine
from models.user import Users as UserModel
from schemas.user import LoginSchema, User
from utility import verify_password
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status, APIRouter
import errors


router = APIRouter(prefix="/auth", tags=["auth"])


async def login_user(email: str, password: str) -> UserModel:
    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.email == email)
        try:
            user = session.exec(statement).one()
            if verify_password(password, user.password):
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=errors.INVALID_CREDENTIALS,
                )
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.INVALID_CREDENTIALS
            )


@router.post("/login", response_model=User, status_code=status.HTTP_200_OK)
async def login(user: LoginSchema) -> User:
    _user: UserModel = await login_user(user.email, user.password)
    return User(**_user.dict())
