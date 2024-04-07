from pydantic import BaseModel


class Token(BaseModel):
    """Model to return token info after authorization"""
    access_token: str
    type: str = "Bearer"
