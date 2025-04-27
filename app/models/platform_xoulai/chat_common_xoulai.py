# models/platform_xoulai/chat_common_xoulai.py
from dataclasses import dataclass, field
from typing import Optional, Any

from dtos.fetch_image_task import FetchImageTask

# TODO: Objectives are missing! Implement them

@dataclass
class ChatLorebookXoulAI:
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
    creator_slug: Optional[str] = None
    asset_type: Optional[str] = None

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task

@dataclass
class ChatCharacterXoulAI:
    slug: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
    voice_id: Optional[str] = None
    talkativeness: Optional[float] = None
    tagline: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None
    backstory: Optional[str] = None
    gender: Optional[str] = None
    samples: Optional[Any] = None

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task



@dataclass
class ChatPersonaXoulAI:
    slug: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
    prompt: Optional[str] = None
    user_slug: Optional[str] = None
    gender: Optional[str] = None
    privilege: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task



@dataclass
class ChatScenarioXoulAI:
    slug: Optional[str] = None
    name: Optional[str] = None
    prompt: list[str] = field(default_factory=list)
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task



@dataclass
class ChatConversationXoulAI:
    conversation_id: Optional[str] = None
    name: Optional[str] = None
    icon_url: Optional[str] = None
    _fetch_image_task: Optional[FetchImageTask] = None
    xoul_voice_id: Optional[str] = None
    narrator_voice: Optional[str] = None
    auto_respond: Optional[bool] = None
    narrate: Optional[bool] = None
    xouls: list[ChatCharacterXoulAI] = field(default_factory=list)
    personas: list[ChatPersonaXoulAI] = field(default_factory=list)
    scenario: Optional[ChatScenarioXoulAI] = None
    objective: Optional[Any] = None
    invite_code: Optional[str] = None
    audio_autoplay: Optional[bool] = None
    lorebook_slug: Optional[str] = None
    lorebook: Optional[ChatLorebookXoulAI] = None
    greeter: Optional[Any] = None
    greeting: Optional[Any] = None
    llm_engine: Optional[str] = None
    talking_style: Optional[str] = None

    def get_public_fields(self) -> dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def set_fetch_image_task(self, fetch_image_task: Optional[FetchImageTask]) -> None:
        self._fetch_image_task = fetch_image_task


@dataclass
class ChatMessageMetadataXoulAI:
    alternative_regenerations: Optional[list[str]] = None
