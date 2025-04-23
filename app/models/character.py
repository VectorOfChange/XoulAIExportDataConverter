# models/character.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Character:
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    icon_url: Optional[str] = None
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
