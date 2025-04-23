# models/all_data.py
from dataclasses import dataclass

from models.character import Character

@dataclass
class AllData:
    characters: list[Character]
    