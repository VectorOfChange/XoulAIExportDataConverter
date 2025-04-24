# models/all_data.py
from dataclasses import dataclass

from models.lorebook import Lorebook
from models.persona import Persona
from models.scenario import Scenario
from models.character import Character

@dataclass
class AllData:
    characters: list[Character]
    scenarios: list[Scenario]
    personas: list[Persona]
    lorebooks: list[Lorebook]
    