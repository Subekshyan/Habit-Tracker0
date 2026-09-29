import math
from datetime import date, timedelta
from typing import Tuple

from sqlalchemy.orm import Session

from . import models

BASE_XP = 10


def streak_multiplier(streak: int) -> float:
    """Longer streaks earn more XP per completion."""
    if streak >= 30:
        return 2.0
    if streak >= 14:
        return 1.75
    if streak >= 7:
        return 1.5
    if streak >= 3:
        return 1.2
    return 1.0


def xp_to_level(total_xp: int) -> int:
    """Level = floor(sqrt(xp) / 10) + 1 - each level takes progressively more XP."""
    return int(math.floor(math.sqrt(total_xp) / 10)) + 1


def xp_for_next_level(level: int) -> int:
    """Minimum total XP needed to reach `level + 1` (inverse of xp_to_level)."""
    return (level * 10) ** 2


def award_xp(db: Session, user: models.User, streak: int) -> Tuple[int, float, bool]:
    """
    Awards XP for a single completion at the given streak length, updates the
    user's level, and grants a freeze token for every level gained.
    Returns (xp_awarded, multiplier_applied, leveled_up).
    """
    multiplier = streak_multiplier(streak)
    xp_awarded = int(BASE_XP * multiplier)

    user.total_xp += xp_awarded
    old_level = user.level
    user.level = xp_to_level(user.total_xp)
    leveled_up = user.level > old_level

    if leveled_up:
        for _ in range(user.level - old_level):
            db.add(models.FreezeToken(user_id=user.id, source="level_up"))

    return xp_awarded, multiplier, leveled_up


def refund_xp(db: Session, user: models.User, xp_amount: int) -> None:
    """Reverses award_xp when a log is undone; re-derives level from the new total."""
    user.total_xp = max(0, user.total_xp - xp_amount)
    user.level = xp_to_level(user.total_xp)


def recompute_streaks(db: Session, habit: models.Habit) -> None:
    """
    Recomputes current_streak, longest_streak, and last_completed_date from
    the full log history for this habit.

    This is doing the same job as the ROW_NUMBER()/LAG() "gap and island"
    window-function query from the original design - grouping consecutive
    dates into unbroken runs - just as a plain linear scan, which is simpler
    to reason about at SQLite scale. A freeze-covered day is stored as a
    real log row (xp_earned=0, used_freeze_token_id set), so it already
    closes the gap for this scan without any special-casing.
    """
    log_dates = sorted(
        log.log_date
        for log in db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit.id)
        .all()
    )

    if not log_dates:
        habit.current_streak = 0
        habit.last_completed_date = None
        return

    longest_run = 1
    current_run = 1

    for previous_date, this_date in zip(log_dates, log_dates[1:]):
        if (this_date - previous_date).days == 1:
            current_run += 1
        else:
            longest_run = max(longest_run, current_run)
            current_run = 1
    longest_run = max(longest_run, current_run)

    last_date = log_dates[-1]
    today = date.today()

    # the streak only counts as "alive" if the most recent log was
    # today or yesterday - anything older means it has lapsed
    habit.current_streak = current_run if last_date in (today, today - timedelta(days=1)) else 0
    habit.longest_streak = max(habit.longest_streak, longest_run)
    habit.last_completed_date = last_date
