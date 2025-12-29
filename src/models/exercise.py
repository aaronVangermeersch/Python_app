from dataclasses import dataclass
from typing import Optional


@dataclass
class Exercise:
    id: Optional[int]
    workout_id: int
    exercise_name: str
    muscle_group: str
    sets: int
    reps: int
    weight: float