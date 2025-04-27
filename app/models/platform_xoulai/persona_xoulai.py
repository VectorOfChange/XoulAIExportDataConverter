# models/platform_xoulai/persona_xoulai.py
from dataclasses import dataclass, fields
from typing import Any, Optional

from dtos.fetch_image_task import FetchImageTask


@dataclass
class PersonaPromptSpecXoulAI:
    age: Optional[int] = None
    gender: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class PersonaXoulAI:
    source_filename: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
    icon_spec: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
    slug: Optional[str] = None
    prompt: Optional[str] = None
    prompt_spec: Optional[PersonaPromptSpecXoulAI] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {}

        for key in data:
            if key in valid_keys:
                if key == "prompt_spec" and isinstance(data[key], dict):
                    filtered_data[key] = PersonaPromptSpecXoulAI(**data[key])
                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}
    
    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task
