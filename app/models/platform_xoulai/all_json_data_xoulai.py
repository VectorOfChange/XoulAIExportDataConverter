# models/platform_xoulai/all_json_data_xoulai.py
from dataclasses import dataclass

from models.platform_xoulai.lorebook_xoulai import LorebookXoulAI
from models.platform_xoulai.persona_xoulai import PersonaXoulAI
from models.platform_xoulai.scenario_xoulai import ScenarioXoulAI
from models.platform_xoulai.character_xoulai import CharacterXoulAI

@dataclass
class AllJsonDataXoulAI:
    characters: list[CharacterXoulAI]
    scenarios: list[ScenarioXoulAI]
    personas: list[PersonaXoulAI]
    lorebooks: list[LorebookXoulAI]
    