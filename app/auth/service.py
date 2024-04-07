from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from starlette import status
from app.config import settings
from app.users.models import User
from app.users.repository import UserRepository, pwd_context
from app.users.schemas import UserCreate
from app.users.service import get_user_repo

# Instance of security class to work with tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# Algorythm that used for encode/decode tokens
ALGORYTHM = "HS256"


def generate_access_token(username: str, token_expires_delta: int | None = 600) -> str:
    """Service function to generate access token
    Parameters
    ----------
    username :
        Username that encodes with 'sub' key
    token_expires_delta :
        Token lifetime, default is 30 minutes

    Returns
    -------
    str :
        A generated token
    """
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


async def check_token(token: str = Depends(oauth2_scheme)) -> str:
    """Check if the token is correct and contains a username string
    Parameters
    ----------
    token :
        A generated token

    Returns
    -------
    str :
        A decoded username from token's 'sub' key
    """
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
    return username


async def check_user_auth(repo: UserRepository = Depends(get_user_repo),
                          username: str = Depends(check_token)) -> User:
    """Check if user authenticated
    Parameters
    ----------
    repo :
        UserRepository class with User CRUD operations'
    username :
        A decoded username from token's 'sub' key

    Returns
    -------
    User :
        A User's class instance
    """
    user = await repo.read(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Username or password not valid")
    return user


async def auth_user(user_data: UserCreate,
                    repo: UserRepository = Depends(get_user_repo)) -> User | None:
    """Check if the user exists and the password are correct
    Parameters
    ----------

    user_data :
        Data of pydantic class UserCreate to get User's username and password
    repo :
        UserRepository class with User CRUD operations'

    Returns
    -------
    User :
        A User's class instance
    """
    user = await repo.read(user_data.username)
    if not (user and pwd_context.verify(user_data.password, user.password)):
        return None
    return user
