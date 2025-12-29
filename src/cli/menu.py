from src.database.db_manager import init_db, insert_workout, insert_exercise
from src.models.workout import Workout
from src.models.exercise import Exercise


def create_workout_with_exercises():
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


def main_menu():
    init_db()

    while True:
        print("=== FITNESSTRACKER ===")
        print("1. Nieuwe training toevoegen")
        print("0. Afsluiten")

        choice = input("Kies een optie: ").strip()

        if choice == "1":
            create_workout_with_exercises()
        elif choice == "0":
            print("Tot ziens!")
            break
        else:
            print("Ongeldige keuze, probeer opnieuw.\n")
