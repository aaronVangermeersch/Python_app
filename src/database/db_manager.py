import sqlite3
import configparser
from pathlib import Path
import csv

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

def get_all_workouts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, date, notes, created_at
            FROM workouts
            ORDER BY date DESC, id DESC
            """
        )
        return cursor.fetchall()
    
def get_exercises_for_workout(workout_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT exercise_name, muscle_group, sets, reps, weight
            FROM exercises
            WHERE workout_id = ?
            ORDER BY id
            """,
            (workout_id,),
        )
        return cursor.fetchall()

def export_workouts_to_csv(csv_path: str):
    with get_connection() as conn, open(
        csv_path, mode="w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "workout_id",
                "date",
                "notes",
                "exercise_name",
                "muscle_group",
                "sets",
                "reps",
                "weight",
            ]
        )

        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                w.id,
                w.date,
                w.notes,
                e.exercise_name,
                e.muscle_group,
                e.sets,
                e.reps,
                e.weight
            FROM workouts w
            LEFT JOIN exercises e ON w.id = e.workout_id
            ORDER BY w.date, w.id, e.id
            """
        )

        for row in cursor.fetchall():
            writer.writerow(row)
