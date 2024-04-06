from typing import Optional
from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import settings
from app.database import get_session
from app.users.models import User
from app.users.service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ALGORYTHM = "HS256"


def generate_access_token(username: str, token_expires_delta: Optional[int] = 30) -> str:
    """Service function to generate access token. Default token lifetime is 30 minutes"""
    expires_time = datetime.now(timezone.utc) + timedelta(minutes=token_expires_delta)
    data_to_encode = {
        "sub": username,
        "exp": expires_time
    }
    token = jwt.encode(
        payload=data_to_encode,
        key=settings.SECRET_JWT_KEY,
        algorithm=ALGORYTHM
    )
    return token


async def check_user_auth(session: AsyncSession = Depends(get_session),
                          token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_JWT_KEY, algorithms=[ALGORYTHM])
        username = payload.get("sub")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token is wrong. "
                                   "Please, enter correct token or get a new token at /auth/login")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token is expired. Please, get new a token at /auth/login")
    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Username or password not valid")
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Username or password not valid")
    return user

