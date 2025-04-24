# models/scenario.py
from dataclasses import dataclass, field, fields
from typing import Optional


@dataclass
class PromptSpec:
    familiarity: Optional[str] = None
    location: Optional[str] = None
    when: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class Meter:
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[int] = 0


@dataclass
class Objective:
    description: Optional[str] = None
    meters: Optional[list[Meter]] = field(default_factory=list)


@dataclass
class Scenario:
    name: Optional[str] = None
    social_tags: Optional[list[str]] = None
    slug: Optional[str] = None
    definition: Optional[str] = None
    greeting: Optional[str] = None
    lorebook_slug: Optional[str] = None
    visibility: Optional[str] = None
    prompt: Optional[str] = None
    prompt_spec: Optional[PromptSpec] = None
    objective: Optional[Objective] = None
    greeter: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {}

        for key in data:
            if key in valid_keys:
                if key == "prompt_spec" and isinstance(data[key], dict):
                    filtered_data[key] = PromptSpec(**data[key])
                elif key == "objective" and isinstance(data[key], dict):
                    meters_data = data[key].get("meters", [])
                    meters = [Meter(**m) for m in meters_data if isinstance(m, dict)]
                    filtered_data[key] = Objective(description=data[key].get("description"), meters=meters)
                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)
