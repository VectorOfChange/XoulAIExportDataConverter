# models/all_data.py
from dataclasses import dataclass
from typing import List

from app.models.character import Character

@dataclass
class AllData:
    characters: List[Character]
    