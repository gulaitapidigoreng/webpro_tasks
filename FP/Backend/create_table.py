# In Backend/create_tables.py

from app.db.database import Base, engine

# IMPORTANT: Import all your models here!
# SQLAlchemy needs to know about them to create the tables.
from app.models import user_model
from app.models import game_model
from app.models import review_model

print("Creating database tables...")

# This line reads all the models that inherited from Base and creates the tables.
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")