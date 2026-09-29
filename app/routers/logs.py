from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(tags=["habit logs"])


@router.post("/habits/{habit_id}/logs", response_model=schemas.CompleteHabitResult)
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    """Log today's completion for a habit: updates streak, awards XP, may level up."""
    return crud.complete_habit(db, habit_id)


@router.get("/habits/{habit_id}/logs", response_model=List[schemas.HabitLogOut])
def list_habit_logs(habit_id: int, db: Session = Depends(get_db)):
    return crud.list_habit_logs(db, habit_id)


@router.delete("/logs/{log_id}", response_model=schemas.UndoLogResult)
def undo_habit_log(log_id: int, db: Session = Depends(get_db)):
    """Undo a completion: deletes the log, refunds its XP, recomputes the streak."""
    return crud.undo_habit_log(db, log_id)
