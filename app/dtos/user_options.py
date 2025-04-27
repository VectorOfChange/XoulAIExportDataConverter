# dtos/user_options.py
from dataclasses import dataclass
from typing import List
import streamlit as st

CONTENT_ORDER = ["characters", "scenarios", "personas", "lorebooks", "chats_single", "chats_multi"]

# TODO: refactor code using this to use new getters/setters
# TODO: Refactor to allow checking if multiple options are present 

@dataclass
class UserOptions:
    selected_content: List[str]
    selected_platforms: List[str]
    selected_formats: List[str]
    fetch_images: bool

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

        fetch_images = st.session_state.get("app_fetch_images", False)

        # Enforce order for content
        content_sorted = [c for c in CONTENT_ORDER if c in content]

        return cls(
            selected_content=content_sorted,
            selected_platforms=platforms,
            selected_formats=formats,
            fetch_images=st.session_state.app_fetch_images
        )

    # Getters for content options
    def is_content_characters_selected(self) -> bool:
        return "characters" in self.selected_content

    def is_content_scenarios_selected(self) -> bool:
        return "scenarios" in self.selected_content

    def is_content_personas_selected(self) -> bool:
        return "personas" in self.selected_content

    def is_content_lorebooks_selected(self) -> bool:
        return "lorebooks" in self.selected_content

    def is_content_chats_single_selected(self) -> bool:
        return "chats_single" in self.selected_content

    def is_content_chats_multi_selected(self) -> bool:
        return "chats_multi" in self.selected_content

    # Getters for platform options
    def is_platform_xoulai_selected(self) -> bool:
        return "xoulai" in self.selected_platforms

    def is_platform_myai_selected(self) -> bool:
        return "myai" in self.selected_platforms

    def is_platform_wyvern_selected(self) -> bool:
        return "wyvern" in self.selected_platforms

    def is_platform_charsnap_selected(self) -> bool:
        return "charsnap" in self.selected_platforms

    def is_platform_sakura_selected(self) -> bool:
        return "sakura" in self.selected_platforms

    def is_platform_tavern_card_selected(self) -> bool:
        return "tavern_card" in self.selected_platforms

    # Getters for format options
    def is_format_word_selected(self) -> bool:
        return "word" in self.selected_formats

    def is_format_txt_selected(self) -> bool:
        return "txt" in self.selected_formats

    def is_format_md_selected(self) -> bool:
        return "md" in self.selected_formats

    def is_format_json_selected(self) -> bool:
        return "json" in self.selected_formats
    
    # Getter for fetch images option
    def is_fetch_images_selected(self) -> bool:
        return self.fetch_images
    
    # Getters for content option property names
    def get_content_characters_property_name(self) -> str:
        return "characters"

    def get_content_scenarios_property_name(self) -> str:
        return "scenarios"

    def get_content_personas_property_name(self) -> str:
        return "personas"

    def get_content_lorebooks_property_name(self) -> str:
        return "lorebooks"

    def get_content_chats_single_property_name(self) -> str:
        return "chats_single"

    def get_content_chats_multi_property_name(self) -> str:
        return "chats_multi"

    # Getters for platform option property names
    def get_platform_xoulai_property_name(self) -> str:
        return "xoulai"

    def get_platform_myai_property_name(self) -> str:
        return "myai"

    def get_platform_wyvern_property_name(self) -> str:
        return "wyvern"

    def get_platform_charsnap_property_name(self) -> str:
        return "charsnap"

    def get_platform_sakura_property_name(self) -> str:
        return "sakura"

    def get_platform_tavern_card_property_name(self) -> str:
        return "tavern_card"

    # Getters for format option property names
    def get_format_word_property_name(self) -> str:
        return "word"

    def get_format_txt_property_name(self) -> str:
        return "txt"

    def get_format_md_property_name(self) -> str:
        return "md"

    def get_format_json_property_name(self) -> str:
        return "json"
