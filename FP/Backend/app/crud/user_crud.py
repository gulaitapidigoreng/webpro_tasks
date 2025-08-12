from sqlalchemy.orm import Session
from app.models import user_model
from app.schemas import user_schema
from app.security import get_password_hash

def get_user(db: Session, user_id: int):
    """Retrieves a single user by their ID."""
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Retrieves a single user by their email."""
    return db.query(user_model.User).filter(user_model.User.email == email).first()
    
def get_user_by_username(db: Session, username: str):
    """Retrieves a single user by their username."""
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def create_user(db: Session, user: user_schema.UserCreate):
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user