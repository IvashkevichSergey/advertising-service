from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from starlette import status
from app.auth.schemas import Token
from app.auth.service import generate_access_token, auth_user
from app.users.repository import UserRepository
from app.users.schemas import UserCreate
from app.users.service import get_user_repo

auth_router = APIRouter(prefix="/auth")


@auth_router.post('/register',
                  summary="Sign up endpoint",
                  status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate,
                        repo: UserRepository = Depends(get_user_repo)):
    """Router for users sign up"""
    user = await repo.read(user_data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Choose another username"})
    user = repo.create(user_data)
    try:
        await repo.session.commit()
        return f"{user.username}, your sign up is finished successfully"
    except IntegrityError as e:
        print(e)
        await repo.session.rollback()


@auth_router.post('/login',
                  summary="Login endpoint",
                  response_model=Token)
async def login_user(user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     repo: UserRepository = Depends(get_user_repo)):
    user = await auth_user(UserCreate(
        username=user_data.username,
        password=user_data.password),
        repo
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Your account is temporarily blocked")
    access_token = generate_access_token(user.username)
    return Token(access_token=access_token)
