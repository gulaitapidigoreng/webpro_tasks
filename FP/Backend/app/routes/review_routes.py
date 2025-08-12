from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud import review_crud
from app.schemas import review_schema, user_schema
from app.auth import get_current_user
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=review_schema.ReviewOut)
def create_review(
    review: review_schema.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(get_current_user)
):
    """
    Create a new review for a game. 
    User must be logged in.
    """
    return review_crud.create_review(db=db, review=review, user_id=current_user.id)

@router.get("/game/{game_id}", response_model=List[review_schema.ReviewOut])
def read_reviews_for_game(game_id: int, db: Session = Depends(get_db)):
    """
    Get all reviews for a specific game. 
    This route is public and does not require login.
    """
    reviews = review_crud.get_reviews_for_game(db, game_id=game_id)
    return reviews

# --- NEW ENDPOINT STARTS HERE ---

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_endpoint(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(get_current_user)
):
    """Deletes a review. A user can only delete their own review."""
    db_review = review_crud.get_review(db, review_id=review_id)

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    review_crud.delete_review(db, review_id=review_id)
    # Return a response upon successful deletion
    return {"detail": "Review deleted successfully"}