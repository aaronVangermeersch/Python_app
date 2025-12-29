# Fitnesstracker CLI

Een eenvoudige command line applicatie om workouts en oefeningen op te slaan in een SQLite-database. 
De applicatie draait in de terminal en gebruikt een settings-bestand om de locatie van de database te bepalen.

## Functionaliteiten

- Nieuwe training toevoegen met datum, optionele notities en meerdere oefeningen.
- Per oefening: naam, spiergroep, aantal sets, reps en gewicht.
- Gegevens worden opgeslagen in twee tabellen: `workouts` en `exercises`.
- Overzicht van alle trainingen en oefeningen in de terminal.
- Export van alle trainingen en oefeningen naar een CSV-bestand 


## Database

De applicatie maakt automatisch (via `init_db`) een SQLite-database aan met twee tabellen:

- `workouts(id, date, notes, created_at)`
- `exercises(id, workout_id, exercise_name, muscle_group, sets, reps, weight, created_at)`

Een workout kan meerdere oefeningen bevatten (relatie 1‑N).

## Gebruik

Voer in een geactiveerde virtual environment uit:

Menu-opties:

- `1` – Nieuwe training toevoegen.
- `2` – Alle trainingen tonen in de terminal.
- `4` – Exporteren naar CSV (`exports/workouts_export.csv`).
- `0` – Afsluiten.

Importeer eventueel het CSV-bestand in Excel om de gegevens verder te bekijken of te analyseren.


