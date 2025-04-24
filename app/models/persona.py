# models/persona.py
from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class PersonaPromptSpec:
    age: Optional[int] = None
    gender: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class Persona:
    name: Optional[str] = None
    slug: Optional[str] = None
    prompt: Optional[str] = None
    prompt_spec: Optional[PersonaPromptSpec] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {}

        for key in data:
            if key in valid_keys:
                if key == "prompt_spec" and isinstance(data[key], dict):
                    filtered_data[key] = PersonaPromptSpec(**data[key])
                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)
