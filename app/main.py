
from fastapi import FastAPI
 
from . import models
from .database import Base, engine
from .routers import analytics, habits, logs, users
 
Base.metadata.create_all(bind=engine)
 
app = FastAPI(
    title="Gamified Habit Tracker & Streak Engine",
    description="Full CRUD backend: users, habits, habit logs, streaks, XP/levels, "
    "freeze tokens, and missed-day analytics.",
    version="2.0.0",
)
 
app.include_router(users.router)
app.include_router(habits.router)
app.include_router(logs.router)
app.include_router(analytics.router)
 
 
@app.get("/", tags=["root"])
def root():
    return {"message": "Habit tracker API is running. Visit /docs for the full API."}
