# models/platform_xoulai/lorebook_xoulai.py
from dataclasses import dataclass, field, fields
from typing import Any, Optional, List

from dtos.fetch_image_task import FetchImageTask


@dataclass
class LorebookSectionXoulAI:
    lore_type: Optional[str] = None
    name: Optional[str] = None
    keywords: Optional[List[str]] = field(default_factory=list)
    text: Optional[str] = None


@dataclass
class LorebookEmbeddedXoulAI:
    asset_type: Optional[str] = None
    sections: Optional[List[LorebookSectionXoulAI]] = field(default_factory=list)

    
@dataclass
class LorebookXoulAI:
    source_filename: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
    social_tags: Optional[List[str]] = None
    visibility: Optional[str] = None
    posted_to_xoul: Optional[str] = None
    posted_to_scenario: Optional[str] = None
    slug: Optional[str] = None
    asset_type: Optional[str] = None
    embedded: Optional[LorebookEmbeddedXoulAI] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {}

        for key in data:
            if key in valid_keys:
                if key == "embedded" and isinstance(data[key], dict):
                    sections_data = data[key].get("sections", [])
                    sections = [LorebookSectionXoulAI(**s) for s in sections_data if isinstance(s, dict)]
                    filtered_data[key] = LorebookEmbeddedXoulAI(
                        asset_type=data[key].get("asset_type"), 
                        sections=sections
                    )
                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)
    
    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}
    
    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task

