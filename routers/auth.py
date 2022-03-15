from models import User
from operations import oauth2
from operations import user_operation as user_op
from schemas.user import ChangePassword, ResetPassSchema, Token, UserBase
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
import errors
from services import get_db
from fastapi.security import OAuth2PasswordRequestForm

from utility import verify_password


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login", response_model=Token)
async def login(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    _user = user_op.authenticate_user(db, user.username, user.password)
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=errors.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = oauth2.create_access_token(data={"user_name": _user.username})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post(
    "/reset", response_model=UserBase, status_code=status.HTTP_205_RESET_CONTENT
)
async def reset_user_password(user: ResetPassSchema, db: Session = Depends(get_db)):
    _user = user_op.reset_password(user, db)
    return _user


@router.post("/change", response_model=UserBase, status_code=status.HTTP_202_ACCEPTED)
async def change_user_password(
    req_body: ChangePassword,
    current_user: User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    if verify_password(req_body.current_password, current_user.password):
        if req_body.new_password == req_body.confirm_password:
            _user = user_op.change_password(current_user, req_body.new_password, db)
            return _user
        else:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=errors.DATA_VALIDATION_FAILED,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=errors.DATA_VALIDATION_FAILED,
        )
