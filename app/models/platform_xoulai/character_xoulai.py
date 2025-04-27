# models/platform_xoulai/character_xoulai.py
from dataclasses import dataclass, fields
from typing import Any, Optional, List

from dtos.fetch_image_task import FetchImageTask

@dataclass
class CharacterXoulAI:
    source_filename: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
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
    
    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}
    
    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task