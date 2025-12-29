from dataclasses import dataclass
from typing import Optional

@dataclass
class Workout:
    id: Optional[int]
    date: str
    notes: str = ""