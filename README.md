# Habit Tracker API

A backend REST API for managing daily habits, tracking completion, calculating streaks, and adding gamification features such as XP, levels, streak multipliers, and freeze tokens.

This project was built using **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic** as a practical backend learning project.

## 🚀 Features

* 👤 User management
* 📝 Create, read, update, and delete habits
* ✅ Mark habits as completed
* 🔥 Automatic streak tracking
* ⭐ XP and level system
* 📈 Streak-based XP multipliers
* 🧊 Freeze tokens for protecting streaks
* 📊 Habit analytics
* 🏆 Leaderboard functionality
* 📅 Daily habit completion tracking
* 🚫 Duplicate completion prevention
* 🗄️ PostgreSQL database
* 🔗 RESTful API architecture
* 📚 Automatic Swagger API documentation

## 🛠️ Tech Stack

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python       | Programming language        |
| FastAPI      | Backend web framework       |
| PostgreSQL   | Relational database         |
| SQLAlchemy   | ORM / database interaction  |
| Pydantic     | Data validation and schemas |
| Uvicorn      | ASGI server                 |
| Alembic      | Database migrations         |
| Git & GitHub | Version control             |

## 📁 Project Structure

```text
Habits/
│
├── venv/
├── requirements.txt
│
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── crud.py
    ├── gamification.py
    │
    └── routers/
        ├── __init__.py
        ├── users.py
        ├── habits.py
        ├── logs.py
        └── analytics.py
```

## 🗄️ Database

The application uses **PostgreSQL** as its database.

Main tables include:

### Users

Stores user information such as:

* User ID
* Name
* Email
* XP
* Level

### Habits

Stores the habits created by users.

Example information:

* Habit ID
* User ID
* Habit name
* Description
* Creation date

### Habit Logs

Stores daily habit completion records.

Used for:

* Completion tracking
* Streak calculation
* Daily history

### Freeze Tokens

Stores freeze tokens that can be used to protect a user's streak when they miss a day.

## 🔥 Streak System

The application calculates consecutive days of habit completion.

For example:

```text
Day 1 → Completed
Day 2 → Completed
Day 3 → Completed
Day 4 → Completed

Current Streak = 4 days
```

If a user misses a day, the streak can be affected depending on the application's freeze-token logic.

## ⭐ Gamification System

The project includes a simple gamification system.

### XP

Users earn experience points by completing habits.

### Levels

XP is converted into user levels.

```text
Complete Habit
      ↓
Earn XP
      ↓
Update Total XP
      ↓
Calculate Level
      ↓
Check for Level Up
```

### Streak Multiplier

Longer streaks can increase the XP earned from completing habits.

This encourages users to maintain consistent habits.

## 🧊 Freeze Tokens

Freeze tokens allow users to protect their streak when they miss a day.

The general flow is:

```text
Habit missed
     ↓
Check freeze tokens
     ↓
Token available?
   ↙       ↘
 Yes        No
 ↓           ↓
Use token   Streak affected
 ↓
Protect streak
```

## 🔄 API Architecture

The application follows a layered backend structure:

```text
Client
  ↓
FastAPI Router
  ↓
CRUD Functions
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
```

### Routers

The `routers/` directory contains API endpoints for different resources.

```text
users.py
habits.py
logs.py
analytics.py
```

### CRUD

`crud.py` contains database operations such as:

* Creating users
* Creating habits
* Updating habits
* Deleting habits
* Completing habits
* Retrieving habit information

### Models

`models.py` defines SQLAlchemy database models.

Python classes are mapped to PostgreSQL tables.

### Schemas

`schemas.py` contains Pydantic models used for:

* Request validation
* Response validation
* Data serialization

### Gamification

`gamification.py` contains the logic for:

* XP calculation
* Level calculation
* Streak multipliers
* Awarding XP
* R

