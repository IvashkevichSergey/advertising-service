from fastapi import APIRouter, Depends
from app.auth.service import check_user_auth
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserBase, UserUpdate
from app.users.service import get_user_repo

user_router = APIRouter(prefix="/users")


@user_router.get('/', response_model=UserBase)
async def get_profile(repo: UserRepository = Depends(get_user_repo),
                      current_user: User = Depends(check_user_auth)):
    """Router for getting current user profile information"""
    return await repo.read(current_user.username)


@user_router.put('/', response_model=UserBase)
async def change_user_info(user_data: UserUpdate,
                           repo: UserRepository = Depends(get_user_repo),
                           current_user: User = Depends(check_user_auth)):
    return await repo.update(user_data, current_user)


@user_router.delete('/')
async def change_user_info(repo: UserRepository = Depends(get_user_repo),
                           current_user: User = Depends(check_user_auth)):
    await repo.delete(current_user.username)
    return f"User {current_user.username} has been deleted successfully"


@user_router.get('/list', response_model=list[UserBase])
async def get_all_users(repo: UserRepository = Depends(get_user_repo)):
    """Router for getting user profile information"""
    return await repo.read_all()
