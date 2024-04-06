from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.schemas import Token
from app.auth.service import check_user_auth, generate_access_token
from app.database import get_session
from app.users.models import User
from app.users.schemas import UserCreate, UserBase, UserUpdate
from app.users.service import get_user_by_username, create_new_user, auth_user, update_user, get_all_users

user_router = APIRouter(prefix="/user")


@user_router.get('/profile/', response_model=UserBase)
def get_me(current_user: User = Depends(check_user_auth)):
    """Router for getting user profile information"""
    return current_user


@user_router.get('/users/')
async def get_me(session: AsyncSession = Depends(get_session)):
    """Router for getting user profile information"""
    return await get_all_users(session)


@user_router.put('/profile/{username}/', response_model=UserBase)
async def change_user_info(username: str,
                           user_data: UserUpdate,
                           session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User is not found")
    return await update_user(session, user_data, user)


