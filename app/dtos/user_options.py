# dtos/user_options.py
from dataclasses import dataclass
from typing import List
import streamlit as st

CONTENT_ORDER = ["characters", "scenarios", "personas", "lorebooks", "chats_single", "chats_multi"]

@dataclass
class UserOptions:
    selected_content: List[str]
    selected_platforms: List[str]
    selected_formats: List[str]

    @classmethod
    def from_session_state(cls):
        content = []
        platforms = []
        formats = []

        for key, value in st.session_state.items():
            if not value:
                continue
            if key.startswith("app_content_"):
                content.append(key.replace("app_content_", ""))
            elif key.startswith("app_platform_"):
                platforms.append(key.replace("app_platform_", ""))
            elif key.startswith("app_format_"):
                formats.append(key.replace("app_format_", ""))

        # Enforce order for content
        content_sorted = [c for c in CONTENT_ORDER if c in content]

        return cls(
            selected_content=content_sorted,
            selected_platforms=platforms,
            selected_formats=formats,
        )
