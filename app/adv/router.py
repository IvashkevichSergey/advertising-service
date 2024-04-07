from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from app import User
from app.adv.repository import AdvRepository
from app.adv.schemas import AdvBase, AdvCreate, AdvUpdate
from app.adv.service import get_adv_repo
from app.auth.service import check_user_auth
from app.comments.router import comment_router
from app.users.permissions import check_owner_or_admin

adv_router = APIRouter(prefix="/adv")
adv_router.include_router(comment_router)


@adv_router.get('/', response_model=list[AdvBase])
async def get_advs(repo: AdvRepository = Depends(get_adv_repo)):
    """Router for getting all advertisements"""
    return await repo.read_all()


@adv_router.get('/{adv_id}', response_model=AdvBase)
async def get_advs(adv_id: int,
                   repo: AdvRepository = Depends(get_adv_repo)):
    """Router for getting all advertisements"""
    adv = await repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    return adv


@adv_router.post('/', response_model=AdvBase)
async def create_adv(adv_data: AdvCreate,
                     repo: AdvRepository = Depends(get_adv_repo),
                     current_user: User = Depends(check_user_auth)):
    """Router for creating a new advertisement"""
    new_adv = repo.create(adv_data, current_user.id)
    try:
        await repo.session.commit()
        return new_adv
    except IntegrityError as e:
        print(e)
        await repo.session.rollback()


@adv_router.put('/{adv_id}', response_model=AdvBase)
async def update_adv(adv_id: int,
                     adv_data: AdvUpdate,
                     repo: AdvRepository = Depends(get_adv_repo),
                     current_user: User = Depends(check_user_auth)):
    """Router for updating info about an advertisement. Accessible only for
    AUTHOR of an advertisement and for ADMIN"""
    adv = await repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    check_owner_or_admin(adv, current_user)
    return await repo.update(adv_data, adv)


@adv_router.delete('/{adv_id}')
async def delete_adv(adv_id: int,
                     repo: AdvRepository = Depends(get_adv_repo),
                     current_user: User = Depends(check_user_auth)):
    """Router for deleting an advertisement. Accessible only for
     AUTHOR of the advertisement and for ADMIN"""
    adv = await repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    check_owner_or_admin(adv, current_user)
    await repo.delete(adv.id)
    return f"Advertisement '{adv.title}' has been deleted successfully"
