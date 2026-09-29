from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(tags=["analytics"])


@router.get("/habits/{habit_id}/missed-days", response_model=schemas.MissedDaysOut)
def missed_days(
    habit_id: int,
    start: date = Query(..., description="Start of range, e.g. 2026-09-01"),
    end: date = Query(..., description="End of range, e.g. 2026-09-30"),
    db: Session = Depends(get_db),
):
    return crud.get_missed_days(db, habit_id, start, end)


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_leaderboard(db, limit=limit)
