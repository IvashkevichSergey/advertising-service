from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.service import check_user_auth
from app.users.models import User, Roles
from app.users.permissions import PermissionChecker
from app.users.repository import UserRepository
from app.users.schemas import UserBase, UserUpdate, UserFullInfo, UserUpdateAdmin
from app.users.service import get_user_repo

user_router = APIRouter(prefix="/users")


@user_router.get('/me', response_model=UserBase)
async def get_user(repo: UserRepository = Depends(get_user_repo),
                   current_user: User = Depends(check_user_auth)):
    """Router for getting current user profile information"""
    res = await repo.read(current_user.username)
    return res


@user_router.put('/me', response_model=UserBase)
async def change_user(user_data: UserUpdate,
                      repo: UserRepository = Depends(get_user_repo),
                      current_user: User = Depends(check_user_auth)):
    """Router for changing current user profile information"""
    return await repo.update(user_data, current_user)


@user_router.delete('/me')
async def delete_user(repo: UserRepository = Depends(get_user_repo),
                      current_user: User = Depends(check_user_auth)):
    """Router for deleting current user"""
    await repo.delete(current_user.username)
    return f"{current_user.username}, your account has been deleted successfully"


@user_router.get('/list',
                 dependencies=[Depends(PermissionChecker([Roles.ADMIN_ROLE]))],
                 response_model=list[UserFullInfo])
async def get_all_users(repo: UserRepository = Depends(get_user_repo)):
    """Router for getting user profile information"""
    return await repo.read_all()


@user_router.post('/change',
                  dependencies=[Depends(PermissionChecker([Roles.ADMIN_ROLE]))],
                  response_model=UserFullInfo)
async def change_users_restricted_data(user_data: UserUpdateAdmin,
                                       repo: UserRepository = Depends(get_user_repo)):
    """Router for changing restricted User information (e.g. role and status) by ADMIN"""
    user = await repo.read(user_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User is not found, check 'username' field")
    return await repo.update_restricted(user_data, user)
