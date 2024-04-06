from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.schemas import Token
from app.auth.service import check_user_auth, generate_access_token
from app.database import get_session
from app.users.models import User
from app.users.schemas import UserCreate, UserBase, UserUpdate
from app.users.service import get_user_by_username, create_new_user, auth_user, update_user

auth_router = APIRouter(prefix="/auth")


@auth_router.post('/register/', status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Router for users sign up"""
    user = await get_user_by_username(session, user_data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "Choose another username"})
    user = create_new_user(session, user_data)
    try:
        await session.commit()
        return f"{user.username}, your sign up is finished successfully"
    except IntegrityError as e:
        print(e)
        await session.rollback()


@auth_router.post('/login/', response_model=Token)
async def login_user(user_data: UserCreate,
                     session: AsyncSession = Depends(get_session)):
    user = await auth_user(session, **user_data.model_dump())
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")
    access_token = generate_access_token(user.username)
    return Token(access_token=access_token)
