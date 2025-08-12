from sqlalchemy.orm import Session
from app.models import review_model
from app.schemas import review_schema

def create_review(db: Session, review: review_schema.ReviewCreate, user_id: int):
    """Creates a review for a game, associated with a user."""
    db_review = review_model.Review(
        **review.dict(), 
        user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_game(db: Session, game_id: int, skip: int = 0, limit: int = 100):
    """Gets all reviews for a specific game."""
    return db.query(review_model.Review).filter(review_model.Review.game_id == game_id).offset(skip).limit(limit).all()

# --- NEW FUNCTIONS START HERE ---

def get_review(db: Session, review_id: int):
    """Gets a single review by its ID."""
    return db.query(review_model.Review).filter(review_model.Review.id == review_id).first()

def delete_review(db: Session, review_id: int):
    """Deletes a review from the database."""
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review