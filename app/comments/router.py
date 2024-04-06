from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import User
from app.adv.repository import AdvRepository
from app.adv.service import get_adv_repo
from app.auth.service import check_user_auth
from app.comments.repository import CommentRepository
from app.comments.schemas import CommentBase, CommentCreate
from app.database import get_session

comment_router = APIRouter()


async def get_comment_repo(session: AsyncSession = Depends(get_session)) -> CommentRepository:
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
                          adv_repo: AdvRepository = Depends(get_adv_repo)):
    adv = await adv_repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    comment = await repo.read(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comment is not found")
    await repo.update(comment_data, comment)
    comments = await repo.read_all(adv_id)
    return comments


@comment_router.delete('/{adv_id}/comments/{comment_id}')
async def delete_comment(adv_id: int,
                         comment_id: int,
                         repo: CommentRepository = Depends(get_comment_repo),
                         adv_repo: AdvRepository = Depends(get_adv_repo)):
    adv = await adv_repo.read(adv_id)
    if not adv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Advertisement is not found")
    comment = await repo.read(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Comment is not found")
    await repo.delete(comment_id)
    return f"Comment '{comment.body}' has been deleted successfully"
