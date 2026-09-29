from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(tags=["habits"])


@router.post("/users/{user_id}/habits", response_model=schemas.HabitOut)
def create_habit(user_id: int, payload: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.create_habit(db, user_id, payload)


@router.get("/habits", response_model=List[schemas.HabitOut])
def list_habits(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.list_habits(db, user_id=user_id)


@router.get("/habits/{habit_id}", response_model=schemas.HabitOut)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    return crud.get_habit_or_404(db, habit_id)


@router.patch("/habits/{habit_id}", response_model=schemas.HabitOut)
def update_habit(habit_id: int, payload: schemas.HabitUpdate, db: Session = Depends(get_db)):
    return crud.update_habit(db, habit_id, payload)


@router.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    crud.delete_habit(db, habit_id)
    return {"message": f"Habit {habit_id} deleted"}
