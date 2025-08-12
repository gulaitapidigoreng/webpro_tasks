from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    platform = Column(String(255), nullable=False)
    release_year = Column(Integer)
    description = Column(Text)
    cover = Column(String(255))
