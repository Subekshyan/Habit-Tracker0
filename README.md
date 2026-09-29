# Habit Tracker API

A backend habit-tracking application built with **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**. The project allows users to create and manage habits, track daily completions, maintain streaks, earn XP, level up, and use freeze tokens to protect their streaks.

## 🚀 Features

* User management
* Create, read, update, and delete habits
* Daily habit completion tracking
* Current and longest streak tracking
* XP and level system
* Streak-based XP multipliers
* Freeze tokens
* Missed-day tracking
* Leaderboard
* Habit analytics
* PostgreSQL database
* SQLAlchemy ORM
* Pydantic data validation
* RESTful API
* Interactive Swagger API documentation

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Pydantic**
* **Uvicorn**

## 📁 Project Structure

```text
Habits/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── gamification.py
│   ├── crud.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       ├── habits.py
│       ├── logs.py
│       └── analytics.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🗄️ Database

The application uses **PostgreSQL** as its database.

The main tables are:

* `users`
* `habits`
* `habit_logs`
* `freeze_tokens`

### Database Relationships

```text
User
 ├── Habits
 │    └── Habit Logs
 │
 └── Freeze Tokens
```

A user can have multiple habits and freeze tokens. Each habit can have multiple completion logs.

## 🎮 Gamification

The application includes a gamification system that rewards users for maintaining consistent habits.

### XP Multipliers

| Streak     | XP Multiplier |
| ---------- | ------------: |
| 0–2 days   |          1.0x |
| 3–6 days   |          1.2x |
| 7–13 days  |          1.5x |
| 14–29 days |         1.75x |
| 30+ days   |          2.0x |

Users earn XP when completing habits and can level up as their total XP increases.

## 🔥 Streak Tracking

The application automatically calculates:

* Current streak
* Longest streak
* Missed days
* Consecutive completion days

The system also supports **freeze tokens**, which can be used to protect a streak when a habit is missed.

## 📚 API Documentation

This project uses FastAPI's automatic API documentation.

After starting the application, open:

```text
http://127.0.0.1:9000/docs
```

This provides an interactive **Swagger UI** where you can test the API endpoints.

The OpenAPI specification is available at:

```text
http://127.0.0.1:9000/openapi.json
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Subekshyan/Habit-Tracker0.git
cd Habit-Tracker0
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ PostgreSQL Configuration

Create a PostgreSQL database and configure the database connection using an environment variable.

Example:

```text
DATABASE_URL=postgresql+psycopg2://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

For security, do **not** upload your `.env` file or database password to GitHub.

## ▶️ Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload --port 9000
```

The API will run at:

```text
http://127.0.0.1:9000
```

Open the interactive API documentation at:

```text
http://127.0.0.1:9000/docs
```

## 🏗️ Architecture

The application follows a layered backend architecture:

```text
Client
   ↓
FastAPI Router
   ↓
CRUD / Business Logic
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL
```

### Main Components

**`main.py`**

Starts the FastAPI application and connects the different routers.

**`database.py`**

Creates the PostgreSQL database connection and SQLAlchemy session.

**`models.py`**

Defines the database tables using SQLAlchemy ORM models.

**`schemas.py`**

Defines and validates API request and response data using Pydantic.

**`crud.py`**

Contains the main database operations such as creating, updating, deleting, and retrieving records.

**`gamification.py`**

Handles XP, levels, streak calculations, and freeze-token logic.

**`routers/`**

Contains the API endpoints for users, habits, logs, and analytics.

## 🎯 Learning Goals

This project was created to practice:

* FastAPI backend development
* REST API development
* PostgreSQL
* SQLAlchemy ORM
* Pydantic
* CRUD operations
* Database relationships
* Dependency injection
* Database transactions
* Backend architecture
* API documentation
* Gamification logic

## 🔮 Future Improvements

Planned improvements include:

* JWT authentication
* User authorization
* Alembic database migrations
* Automated testing
* Docker containerization
* Frontend application
* Cloud deployment
* CI/CD pipeline

## 👩‍💻 Author

**Subekshya Neupane**

Data Science & AI Enthusiast

Built as a hands-on backend project to strengthen skills in **Python, FastAPI, PostgreSQL, and API development**.
