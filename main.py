from src.database.db_manager import init_db, insert_workout, insert_exercise
from src.models.workout import Workout
from src.models.exercise import Exercise


def main():
    init_db()

    workout = Workout(id=None, date="2025-12-29", notes="Test training")
    workout_id = insert_workout(workout)

    exercise = Exercise(
        id=None,
        workout_id=workout_id,
        exercise_name="Bench Press",
        muscle_group="Chest",
        sets=3,
        reps=8,
        weight=80.0,
    )
    insert_exercise(exercise)

    print("Test workout + exercise inserted.")


if __name__ == "__main__":
    main()
