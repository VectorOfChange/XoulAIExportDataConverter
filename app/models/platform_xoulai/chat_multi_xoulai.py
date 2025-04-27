# models/platform_xoulai/chat_multi_xoulai.py
from dataclasses import dataclass, field, fields
import json
import textwrap
from typing import Optional, Any, List
from utils.custom_logger import log
from models.platform_xoulai.chat_common_xoulai import ChatCharacterXoulAI, ChatConversationXoulAI, ChatMessageMetadataXoulAI, ChatPersonaXoulAI, ChatScenarioXoulAI

@dataclass
class ChatMultiMessageXoulAI:
    message_id: Optional[int] = None
    conversation_id: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[str] = None
    author_slug: Optional[str] = None
    author_type: Optional[str] = None
    author_name: Optional[str] = None
    editor_name: Optional[str] = None
    content_type: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[ChatMessageMetadataXoulAI] = None
    references_id: Optional[Any] = None

@dataclass
class ChatMultiXoulAI:
    conversation: Optional[ChatConversationXoulAI] = None
    messages: List[ChatMultiMessageXoulAI] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMultiXoulAI":
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {}

        for key in data:
            if key in valid_keys:
                if key == "conversation" and isinstance(data[key], dict):
                    conversation_data = data[key]
                    conversation_fields = {f.name for f in fields(ChatConversationXoulAI)}
                    filtered_conversation = {}

                    for c_key in conversation_data:
                        if c_key in conversation_fields:
                            if c_key == "xouls" and isinstance(conversation_data[c_key], list):
                                filtered_conversation[c_key] = [ChatCharacterXoulAI(**x) for x in conversation_data[c_key] if isinstance(x, dict)]
                            elif c_key == "personas" and isinstance(conversation_data[c_key], list):
                                filtered_conversation[c_key] = [ChatPersonaXoulAI(**p) for p in conversation_data[c_key] if isinstance(p, dict)]
                            elif c_key == "scenario" and isinstance(conversation_data[c_key], dict):
                                filtered_conversation[c_key] = ChatScenarioXoulAI(**{k: v for k, v in conversation_data[c_key].items() if k in {f.name for f in fields(ChatScenarioXoulAI)}})
                            else:
                                filtered_conversation[c_key] = conversation_data[c_key]

                    filtered_data[key] = ChatConversationXoulAI(**filtered_conversation)

                elif key == "messages" and isinstance(data[key], list):
                    messages = []
                    for message_data in data[key]:
                        message_fields = {f.name for f in fields(ChatMultiMessageXoulAI)}
                        filtered_message = {}

                        for m_key, m_value in message_data.items():
                            if m_key in message_fields:
                                if m_key == "metadata":
                                    if isinstance(m_value, dict):
                                        metadata_fields = {f.name for f in fields(ChatMessageMetadataXoulAI)}
                                        filtered_metadata = {
                                            k: v for k, v in m_value.items() if k in metadata_fields
                                        }
                                        filtered_message[m_key] = ChatMessageMetadataXoulAI(**filtered_metadata)
                                    elif isinstance(m_value, str):
                                        try:
                                            metadata_dict = json.loads(m_value)
                                            metadata_fields = {f.name for f in fields(ChatMessageMetadataXoulAI)}
                                            filtered_metadata = {
                                                k: v for k, v in metadata_dict.items() if k in metadata_fields
                                            }
                                            filtered_message[m_key] = ChatMessageMetadataXoulAI(**filtered_metadata)
                                        except json.JSONDecodeError:
                                            log(f"Warning: Could not decode metadata string: {m_value}")
                                else:
                                    filtered_message[m_key] = message_data[m_key]

                        messages.append(ChatMultiMessageXoulAI(**filtered_message))
                    filtered_data[key] = messages

                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)

    def get_chat_description(self) -> Optional[list[str]]:
        description = []
        
        if self.conversation:
            description.append(f"Group Chat: {self.get_conversation_name()}")
            description.append(f"Characters: {', '.join(self.get_character_names())}")
            description.append(f"Personas: {', '.join(self.get_persona_names())}")
        else:
            description.append("ERROR: Conversation Data Missing")
        
        return description

    def get_character_names(self, return_none_if_empty: bool = False) -> list[str]:
        """
        Returns a list of character names.

        Args:
            return_none_if_empty: If True, returns None if there are no character names.
                                If False (default), returns a list containing "No named characters".
        """
        names = []
        if self.conversation and self.conversation.xouls:
            names = [character.name for character in self.conversation.xouls]
        elif not return_none_if_empty:
            names = ["No named characters"]

        return names

    def get_persona_names(self, return_none_if_empty: bool = False) -> list[str]:
            """
            Returns a list of persona names.

            Args:
                return_none_if_empty: If True, returns None if there are no persona names.
                                    If False (default), returns a list containing "No named personas".
            """
            names = []
            if self.conversation and self.conversation.personas:
                names = [persona.name for persona in self.conversation.personas]
            elif not return_none_if_empty:
                names = ["No named personas"]

            return names

    def get_conversation_name(self) -> str:
        if self.conversation and self.conversation.name:
            return f"{self.conversation.name}"
        else:
            return "Unnamed Group Chat"
