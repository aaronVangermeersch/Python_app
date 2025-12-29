from pathlib import Path

from src.database.db_manager import (
    init_db,
    insert_workout,
    insert_exercise,
    get_all_workouts,
    get_exercises_for_workout,
    export_workouts_to_csv,
)
from src.models.workout import Workout
from src.models.exercise import Exercise


def create_workout_with_exercises():
    print()
    date = input("Datum van de training (YYYY-MM-DD): ")
    notes = input("Notities (optioneel): ")

    workout = Workout(id=None, date=date, notes=notes)
    workout_id = insert_workout(workout)
    print(f"Training aangemaakt met id {workout_id}.")

    while True:
        add_ex = input("Oefening toevoegen? (j/n): ").strip().lower()
        if add_ex != "j":
            break

        name = input("Naam oefening: ")
        muscle = input("Spiergroep: ")
        sets = int(input("Aantal sets: "))
        reps = int(input("Aantal reps per set: "))
        weight = float(input("Gewicht (kg): "))

        exercise = Exercise(
            id=None,
            workout_id=workout_id,
            exercise_name=name,
            muscle_group=muscle,
            sets=sets,
            reps=reps,
            weight=weight,
        )
        insert_exercise(exercise)
        print("Oefening opgeslagen.")

    print("Training compleet opgeslagen.\n")


def show_all_workouts():
    workouts = get_all_workouts()
    if not workouts:
        print("Geen trainingen gevonden.\n")
        return

    for wid, date, notes, created_at in workouts:
        print(f"\nTraining {wid} - {date}")
        if notes:
            print(f"  Notities: {notes}")
        exercises = get_exercises_for_workout(wid)
        if not exercises:
            print("  (Geen oefeningen)")
            continue
        for name, muscle, sets, reps, weight in exercises:
            print(f"  - {name} ({muscle}): {sets} x {reps} @ {weight} kg")
    print()


def export_to_csv():
    base_dir = Path(__file__).resolve().parents[2]
    export_dir = base_dir / "exports"
    export_dir.mkdir(exist_ok=True)

    csv_path = export_dir / "workouts_export.csv"
    export_workouts_to_csv(str(csv_path))
    print(f"Export voltooid: {csv_path}\n")


def main_menu():
    init_db()

    while True:
        print("=== FITNESSTRACKER ===")
        print("1. Nieuwe training toevoegen")
        print("2. Alle trainingen tonen")
        print("3. Exporteren naar CSV")
        print("0. Afsluiten")

        choice = input("Kies een optie: ").strip()

        if choice == "1":
            create_workout_with_exercises()
        elif choice == "2":
            show_all_workouts()
        elif choice == "3":
            export_to_csv()
        elif choice == "0":
            print("Tot ziens!")
            break
        else:
            print("Ongeldige keuze, probeer opnieuw.\n")
