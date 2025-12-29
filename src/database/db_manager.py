import sqlite3
import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
SETTINGS_FILE = BASE_DIR / "settings.ini"

config = configparser.ConfigParser()
config.read(SETTINGS_FILE)

db_path = BASE_DIR / config["database"]["DB_PATH"]

def get_connection():
    return sqlite3.connect(db_path)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER NOT NULL,
                exercise_name TEXT NOT NULL,
                muscle_group TEXT NOT NULL,
                sets INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                weight REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workout_id) REFERENCES workouts (id)
            );
            """
        )

        conn.commit()
        
from src.models.workout import Workout
from src.models.exercise import Exercise

def insert_workout(workout: Workout) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
          INSERT INTO workouts (date, notes)
          VALUES (?, ?)
          """,
          (workout.date, workout.notes),
            )
        conn.commit()
        return cursor.lastrowid
    
def insert_exercise(exercise: Exercise) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO exercises (
                workout_id,
                exercise_name,
                muscle_group,
                sets,
                reps,
                weight
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                exercise.workout_id,
                exercise.exercise_name,
                exercise.muscle_group,
                exercise.sets,
                exercise.reps,
                exercise.weight,
            ),
            )
        
        conn.commit()
        return cursor.lastrowid        
        