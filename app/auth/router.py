from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from app.auth.schemas import Token
from app.auth.service import generate_access_token, auth_user
from app.users.repository import UserRepository
from app.users.schemas import UserCreate
from app.users.service import get_user_repo

auth_router = APIRouter(prefix="/auth")


@auth_router.post('/register/', status_code=status.HTTP_201_CREATED)
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


@auth_router.post('/login/', response_model=Token)
async def login_user(user_data: UserCreate,
                     repo: UserRepository = Depends(get_user_repo)):
    user = await auth_user(user_data, repo)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")
    access_token = generate_access_token(user.username)
    return Token(access_token=access_token)
