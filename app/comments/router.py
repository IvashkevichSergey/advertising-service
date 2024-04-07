from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app import User
from app.adv.models import Group
from app.adv.repository import AdvRepository
from app.adv.service import get_adv_repo
from app.auth.service import check_user_auth
from app.comments.repository import CommentRepository
from app.comments.schemas import CommentBase, CommentCreate
from app.database import get_session
from app.users.models import Roles
from app.users.permissions import check_owner_or_admin, PermissionChecker

comment_router = APIRouter()


async def get_comment_repo(session: AsyncSession = Depends(get_session)) -> CommentRepository:
    """Service function to return class with Comment CRUD operations"""
    return CommentRepository(session)


@comment_router.get('/{adv_id}/comments', response_model=list[CommentBase] | None)
async def get_comments(adv_id: int,
                       repo: CommentRepository = Depends(get_comment_repo)):
    """Router for getting all comments of any advertisement"""
    comments = await repo.read_all(adv_id)
    return comments


@comment_router.post('/{adv_id}/comments', response_model=list[CommentBase])
async def create_comment(comment_data: CommentCreate,
                         adv_id: int,
                         repo: CommentRepository = Depends(get_comment_repo),
                         adv_repo: AdvRepository = Depends(get_adv_repo),
                         current_user: User = Depends(check_user_auth)):
    """Router for creating a new comment"""
    adv = await adv_repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    repo.create(comment_data, current_user.id, adv_id)
    try:
        await repo.session.commit()
        comments = await repo.read_all(adv_id)
        return comments
    except IntegrityError as e:
        print(e)
        await repo.session.rollback()


@comment_router.put('/{adv_id}/comments/{comment_id}', response_model=list[CommentBase])
async def update_comments(adv_id: int,
                          comment_id: int,
                          comment_data: CommentCreate,
                          repo: CommentRepository = Depends(get_comment_repo),
                          adv_repo: AdvRepository = Depends(get_adv_repo),
                          current_user: User = Depends(check_user_auth)):
    """Router for changing a comment. Accessible only for
    AUTHOR of the comment and for ADMIN"""
    adv = await adv_repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    comment = await repo.read(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comment is not found")
    check_owner_or_admin(comment, current_user)
    await repo.update(comment_data, comment)
    comments = await repo.read_all(adv_id)
    return comments


@comment_router.delete('/{adv_id}/comments/{comment_id}')
async def delete_comment(adv_id: int,
                         comment_id: int,
                         repo: CommentRepository = Depends(get_comment_repo),
                         adv_repo: AdvRepository = Depends(get_adv_repo),
                         current_user: User = Depends(check_user_auth)):
    """Router for deleting a comment. Accessible only for
     AUTHOR of the comment and for ADMIN"""
    adv = await adv_repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    comment = await repo.read(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comment is not found")
    check_owner_or_admin(adv, current_user)
    await repo.delete(comment_id)
    return f"Comment '{comment.body}' has been deleted successfully"


@comment_router.delete('/del_comments/{adv_group}',
                       dependencies=[Depends(PermissionChecker([Roles.ADMIN_ROLE]))])
async def delete_comments(adv_group: Group,
                         repo: CommentRepository = Depends(get_comment_repo)):
    """Router for deleting all comments from specific Adv Group.
    Accessible only for ADMIN"""
    res = await repo.delete_group(adv_group)
    if not res:
        return f"No comments to delete from '{adv_group}' group advertisements"
    return f"{res} comment(-s) deleted from '{adv_group}' group advertisements"
