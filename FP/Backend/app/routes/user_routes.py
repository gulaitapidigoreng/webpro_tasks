from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import user_schema
from app.auth import get_current_user
from app.db.database import get_db

router = APIRouter()

@router.get("/me", response_model=user_schema.UserOut)
def read_users_me(current_user: user_schema.UserOut = Depends(get_current_user)):
    """
    Fetch the profile of the currently logged-in user.
    """
    return current_user