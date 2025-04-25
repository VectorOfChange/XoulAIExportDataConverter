# models/platform_xoulai/all_data_xoulai.py
from dataclasses import dataclass, field

from enums.platform import Platform
from models.platform_xoulai.lorebook_xoulai import LorebookXoulAI
from models.platform_xoulai.persona_xoulai import PersonaXoulAI
from models.platform_xoulai.scenario_xoulai import ScenarioXoulAI
from models.platform_xoulai.character_xoulai import CharacterXoulAI

@dataclass
class AllDataXoulAI:
    platform: Platform = field(init=False, default=Platform.XOULAI)
    characters: list[CharacterXoulAI]
    scenarios: list[ScenarioXoulAI]
    personas: list[PersonaXoulAI]
    lorebooks: list[LorebookXoulAI]
    