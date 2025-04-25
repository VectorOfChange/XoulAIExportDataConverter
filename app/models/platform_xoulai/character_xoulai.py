# models/platform_xoulai/character_xoulai.py
from dataclasses import dataclass, fields
from typing import Optional, List

@dataclass
class CharacterXoulAI:
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    tagline: Optional[str] = None
    social_tags: Optional[List[str]] = None
    slug: Optional[str] = None
    bio: Optional[str] = None
    backstory: Optional[str] = None
    backstory_spec: Optional[str] = None
    definition: Optional[str] = None
    default_scenario: Optional[str] = None
    samples: Optional[str] = None
    greeting: Optional[str] = None
    talking_style: Optional[str] = None
    lorebook_slug: Optional[str] = None
    visibility: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)