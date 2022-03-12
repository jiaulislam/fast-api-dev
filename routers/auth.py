from tokenize import Token
from schemas.user import Token
from models import User
from fastapi import HTTPException, status, APIRouter, Depends
import errors
from fastapi.security import OAuth2PasswordRequestForm

from utility import verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    _user: User = await authenticate_user(form_data.username, form_data.password)
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=errors.INVALID_CREDENTIALS,
            headers={'WWW-Authenticate': "Bearer"}
        )

    if not verify_password(form_data.password, _user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=errors.INVALID_CREDENTIALS,
            headers={'WWW-Authenticate': "Bearer"}
        )

    access_token = create_access_token(data={"sub": _user.username})
    return {"access_token": access_token, "token_type": "Bearer"}