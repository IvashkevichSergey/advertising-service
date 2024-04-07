from fastapi import Depends, HTTPException
from starlette import status
from app import User, Adv
from app.auth.service import check_user_auth
from app.comments.models import Comment
from app.users.models import Roles


class PermissionChecker:
    """Class is used by Dependencies to check if user's role has right permissions"""
    def __init__(self, access_roles_list: list[str]):
        self.access_roles = access_roles_list

    def __call__(self, current_user: User = Depends(check_user_auth)):
        for role in self.access_roles:
            if role not in current_user.role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="You don't have access")
        return True


def check_owner_or_admin(item_instance: Adv | Comment, user_instance: User) -> bool:
    """Check user permission to get access to some methods (e.g. put, delete)"""
    if (item_instance.author_id == user_instance.id) \
            or (user_instance.role == Roles.ADMIN_ROLE):
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="You don't have access")
