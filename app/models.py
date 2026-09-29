from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)

    total_xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habits = relationship(
        "Habit", back_populates="owner", cascade="all, delete-orphan"
    )
    freeze_tokens = relationship(
        "FreezeToken", back_populates="owner", cascade="all, delete-orphan"
    )


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    frequency_type = Column(String, default="daily", nullable=False)  # "daily" | "weekly"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_completed_date = Column(Date, nullable=True)

    owner = relationship("User", back_populates="habits")
    logs = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )


class HabitLog(Base):
    __tablename__ = "habit_logs"
    __table_args__ = (
        # A habit can only be logged once per calendar date -
        # this is what actually prevents duplicate completions.
        UniqueConstraint("habit_id", "log_date", name="uq_habit_logdate"),
    )

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)

    # set when this specific day was "saved" by a freeze token rather
    # than actually being completed by the user
    used_freeze_token_id = Column(
        Integer, ForeignKey("freeze_tokens.id"), nullable=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="logs")


class FreezeToken(Base):
    __tablename__ = "freeze_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    source = Column(String, default="level_up", nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    consumed_at = Column(DateTime, nullable=True)  # NULL = still available

    owner = relationship("User", back_populates="freeze_tokens")
