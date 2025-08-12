from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text # <-- Make sure this is imported
from typing import List

from app.crud import game_crud
from app.schemas import game_schema, user_schema
from app.db.database import get_db
from app.auth import get_current_user

router = APIRouter()

# --- THIS FUNCTION IS UPDATED ---
@router.post("/", response_model=game_schema.GameOut)
def create_game(
    game: game_schema.GameCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.UserOut = Depends(get_current_user)
):
    # --- SPECIAL SCENARIO ---
    if game.title.lower() == "gundam sd":
        # WARNING: Destructive Action!
        # 1. Delete all existing reviews
        db.execute(text("DELETE FROM reviews"))
        # 2. Delete all existing games
        db.execute(text("DELETE FROM games"))
        db.commit()
        
        # 3. Create only the "Gundam SD" game
        gundam_game = game_crud.create_game(db=db, game=game)
        return gundam_game
    
    # --- NORMAL OPERATION ---
    else:
        # If the title is not "Gundam SD", create the game normally
        return game_crud.create_game(db=db, game=game)

# --- THE REST OF THE FILE REMAINS THE SAME ---
@router.get("/", response_model=List[game_schema.GameOut])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = game_crud.get_games(db, skip=skip, limit=limit)
    return games

@router.get("/{game_id}", response_model=game_schema.GameOut)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game