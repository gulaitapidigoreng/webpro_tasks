from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORT THIS

# Your routes (removed duplicate review_routes import)
from app.routes import auth_routes, game_routes, review_routes, user_routes

app = FastAPI(title="Game Review Site API")

# Define the list of origins that are allowed to make requests
# This should be the address your frontend is running on
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

# Add the CORS middleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes (removed duplicate review_routes router)
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(game_routes.router, prefix="/api/games", tags=["Games"])
app.include_router(review_routes.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to the Project: Game Review Site"}

# The if __name__ == "__main__": block has been removed for clarity.
# It's best to run the server using the terminal command:
# uvicorn app.main:app --reload