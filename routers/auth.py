from tokenize import Token
from operations.user_operation import authenticate_user, create_access_token
from schemas.user import User, Token
from fastapi import HTTPException, status, APIRouter, Depends
import errors
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    _user: User = await authenticate_user(form_data.username, form_data.password)
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=errors.INVALID_CREDENTIALS,
            headers={'WWW-Authenticate': "Bearer"}
        )

    access_token = create_access_token(data={"sub": _user.username})
    return {"access_token": access_token, "token_type": "Bearer"}