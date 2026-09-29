from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import gamification, models, schemas

# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def create_user(db: Session, payload: schemas.UserCreate) -> models.User:
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = models.User(username=payload.username, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_or_404(db: Session, user_id: int) -> models.User:
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def list_users(db: Session) -> List[models.User]:
    return db.query(models.User).order_by(models.User.id).all()


def update_user(db: Session, user_id: int, payload: schemas.UserUpdate) -> models.User:
    user = get_user_or_404(db, user_id)
    if payload.username is not None:
        user.username = payload.username
    if payload.email is not None:
        user.email = payload.email
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_or_404(db, user_id)
    db.delete(user)
    db.commit()


def get_leaderboard(db: Session, limit: int = 10) -> List[schemas.LeaderboardEntry]:
    users = (
        db.query(models.User)
        .order_by(models.User.total_xp.desc())
        .limit(limit)
        .all()
    )
    return [
        schemas.LeaderboardEntry(
            rank=i + 1, username=u.username, total_xp=u.total_xp, level=u.level
        )
        for i, u in enumerate(users)
    ]


def list_freeze_tokens(db: Session, user_id: int) -> List[models.FreezeToken]:
    get_user_or_404(db, user_id)
    return (
        db.query(models.FreezeToken)
        .filter(models.FreezeToken.user_id == user_id)
        .order_by(models.FreezeToken.earned_at)
        .all()
    )


# ---------------------------------------------------------------------------
# Habits
# ---------------------------------------------------------------------------

def create_habit(db: Session, user_id: int, payload: schemas.HabitCreate) -> models.Habit:
    get_user_or_404(db, user_id)
    habit = models.Habit(
        user_id=user_id, name=payload.name, frequency_type=payload.frequency_type
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def get_habit_or_404(db: Session, habit_id: int) -> models.Habit:
    habit = db.get(models.Habit, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


def list_habits(db: Session, user_id: Optional[int] = None) -> List[models.Habit]:
    query = db.query(models.Habit)
    if user_id is not None:
        query = query.filter(models.Habit.user_id == user_id)
    return query.order_by(models.Habit.id).all()


def update_habit(db: Session, habit_id: int, payload: schemas.HabitUpdate) -> models.Habit:
    habit = get_habit_or_404(db, habit_id)
    if payload.name is not None:
        habit.name = payload.name
    if payload.frequency_type is not None:
        habit.frequency_type = payload.frequency_type
    if payload.is_active is not None:
        habit.is_active = payload.is_active
    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(db: Session, habit_id: int) -> None:
    habit = get_habit_or_404(db, habit_id)
    db.delete(habit)
    db.commit()


# ---------------------------------------------------------------------------
# Habit logs (completion / undo / history)
# ---------------------------------------------------------------------------

def list_habit_logs(db: Session, habit_id: int) -> List[models.HabitLog]:
    get_habit_or_404(db, habit_id)
    return (
        db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit_id)
        .order_by(models.HabitLog.log_date)
        .all()
    )


def complete_habit(db: Session, habit_id: int) -> schemas.CompleteHabitResult:
    """
    The core gamified action: mark a habit done for today.
      1. Reject a second completion on the same day.
      2. If exactly one day was missed and a freeze token is available,
         auto-consume it to silently backfill that missed day.
      3. Insert today's log, recompute the streak from full history.
      4. Award XP (scaled by the new streak) and update the user's level.
    All of this happens inside one DB transaction - either the whole
    sequence commits, or none of it does.
    """
    habit = get_habit_or_404(db, habit_id)
    user = habit.owner
    today = date.today()

    already_logged = (
        db.query(models.HabitLog)
        .filter(models.HabitLog.habit_id == habit_id, models.HabitLog.log_date == today)
        .first()
    )
    if already_logged:
        raise HTTPException(status_code=400, detail="Habit already logged today")

    freeze_used = False
    if habit.last_completed_date is not None:
        gap = (today - habit.last_completed_date).days
        if gap == 2:  # exactly one day was missed
            available_token = (
                db.query(models.FreezeToken)
                .filter(
                    models.FreezeToken.user_id == user.id,
                    models.FreezeToken.consumed_at.is_(None),
                )
                .first()
            )
            if available_token:
                missed_date = habit.last_completed_date + timedelta(days=1)
                db.add(
                    models.HabitLog(
                        habit_id=habit.id,
                        log_date=missed_date,
                        xp_earned=0,
                        used_freeze_token_id=available_token.id,
                    )
                )
                available_token.consumed_at = datetime.utcnow()
                freeze_used = True

    today_log = models.HabitLog(habit_id=habit.id, log_date=today, xp_earned=0)
    db.add(today_log)
    db.flush()  # so recompute_streaks sees today's row too

    gamification.recompute_streaks(db, habit)
    xp_awarded, multiplier, leveled_up = gamification.award_xp(db, user, habit.current_streak)
    today_log.xp_earned = xp_awarded

    db.commit()
    db.refresh(habit)
    db.refresh(user)

    return schemas.CompleteHabitResult(
        habit=schemas.HabitOut.model_validate(habit),
        xp_awarded=xp_awarded,
        multiplier_applied=multiplier,
        leveled_up=leveled_up,
        freeze_token_auto_used=freeze_used,
        xp_to_next_level=max(0, gamification.xp_for_next_level(user.level) - user.total_xp),
        user_total_xp=user.total_xp,
        user_level=user.level,
    )


def undo_habit_log(db: Session, log_id: int) -> schemas.UndoLogResult:
    """
    Deletes a log entry, refunds its XP from the owning user, and
    recomputes the habit's streak - so an accidental log doesn't leave
    the user's XP/level or the habit's streak inconsistent.
    """
    log = db.get(models.HabitLog, log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    habit = get_habit_or_404(db, log.habit_id)
    user = habit.owner
    xp_refunded = log.xp_earned

    db.delete(log)
    db.flush()

    gamification.refund_xp(db, user, xp_refunded)
    gamification.recompute_streaks(db, habit)

    db.commit()
    db.refresh(habit)

    return schemas.UndoLogResult(
        habit=schemas.HabitOut.model_validate(habit), xp_refunded=xp_refunded
    )


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def get_missed_days(
    db: Session, habit_id: int, start: date, end: date
) -> schemas.MissedDaysOut:
    """
    Calendar gap analysis: generates every date in [start, end] and
    subtracts the dates that actually have a log - the same idea as
    generate_series() LEFT JOIN habit_logs, done in Python.
    """
    get_habit_or_404(db, habit_id)
    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")

    logged_dates = {
        log.log_date
        for log in db.query(models.HabitLog)
        .filter(
            models.HabitLog.habit_id == habit_id,
            models.HabitLog.log_date >= start,
            models.HabitLog.log_date <= end,
        )
        .all()
    }

    today = date.today()
    all_dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    missed = [d for d in all_dates if d not in logged_dates and d <= today]

    return schemas.MissedDaysOut(
        habit_id=habit_id,
        start=start,
        end=end,
        missed_dates=missed,
        missed_count=len(missed),
    )
