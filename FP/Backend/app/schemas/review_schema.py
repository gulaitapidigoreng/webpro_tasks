from pydantic import BaseModel
from typing import Optional
from .user_schema import UserOut # Import UserOut to nest user info

class ReviewBase(BaseModel):
    rating: int
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    game_id: int

class ReviewUpdate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int
    user_id: int
    game_id: int
    owner: UserOut # This will nest the user's public info in the response

    class Config:
        from_attributes = True