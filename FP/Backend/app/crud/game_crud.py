# In app/crud/game_crud.py
from sqlalchemy.orm import Session
from app.models import game_model
from app.schemas import game_schema

# Function to get a single game by its ID
def get_game(db: Session, game_id: int):
    return db.query(game_model.Game).filter(game_model.Game.id == game_id).first()

# Function to get a list of all games
def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(game_model.Game).offset(skip).limit(limit).all()

# Function to create a new game
def create_game(db: Session, game: game_schema.GameCreate):
    db_game = game_model.Game(
        title=game.title,
        genre=game.genre,
        platform=game.platform,
        release_year=game.release_year,
        description=game.description,
        cover=game.cover
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game