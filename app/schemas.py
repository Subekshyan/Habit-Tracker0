from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[str]
    total_xp: int
    level: int
    created_at: datetime


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    total_xp: int
    level: int


# ---------------------------------------------------------------------------
# Habits
# ---------------------------------------------------------------------------

class HabitCreate(BaseModel):
    name: str
    frequency_type: str = "daily"  # "daily" | "weekly"


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency_type: Optional[str] = None
    is_active: Optional[bool] = None


class HabitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    frequency_type: str
    is_active: bool
    current_streak: int
    longest_streak: int
    last_completed_date: Optional[date]
    created_at: datetime


# ---------------------------------------------------------------------------
# Habit logs
# ---------------------------------------------------------------------------

class HabitLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    log_date: date
    xp_earned: int
    used_freeze_token_id: Optional[int]


class CompleteHabitResult(BaseModel):
    habit: HabitOut
    xp_awarded: int
    multiplier_applied: float
    leveled_up: bool
    freeze_token_auto_used: bool
    xp_to_next_level: int
    user_total_xp: int
    user_level: int


class UndoLogResult(BaseModel):
    habit: HabitOut
    xp_refunded: int


# ---------------------------------------------------------------------------
# Freeze tokens
# ---------------------------------------------------------------------------

class FreezeTokenOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    earned_at: datetime
    consumed_at: Optional[datetime]


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

class MissedDaysOut(BaseModel):
    habit_id: int
    start: date
    end: date
    missed_dates: List[date]
    missed_count: int
