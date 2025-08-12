from pydantic import BaseModel
from typing import Optional

class GameBase(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: Optional[int] = None
    description: Optional[str] = None
    cover: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    pass

class GameOut(GameBase):
    id: int

    class Config:
        from_attributes = True
