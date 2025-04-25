# models/platform_xoulai/persona_xoulai.py
from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class PersonaPromptSpecXoulAI:
    age: Optional[int] = None
    gender: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class PersonaXoulAI:
    name: Optional[str] = None
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
