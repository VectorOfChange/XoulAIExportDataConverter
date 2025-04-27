# models/platform_xoulai/chat_single_xoulai.py
from dataclasses import dataclass, field, fields
from typing import Optional, Any
from models.platform_xoulai.chat_common_xoulai import ChatCharacterXoulAI, ChatConversationXoulAI, ChatLorebookXoulAI, ChatMessageMetadataXoulAI, ChatPersonaXoulAI, ChatScenarioXoulAI

@dataclass
class ChatSingleMessageXoulAI:
    role: Optional[str] = None
    content: Optional[str] = None
    name: Optional[str] = None
    turn_id: Optional[int] = None
    timestamp: Optional[str] = None
    metadata: ChatMessageMetadataXoulAI = field(default_factory=ChatMessageMetadataXoulAI)

@dataclass
class ChatSingleXoulAI:
    conversation: Optional[ChatConversationXoulAI] = None
    messages: list[ChatSingleMessageXoulAI] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatSingleXoulAI":
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
                                filtered_conversation[c_key] = ChatScenarioXoulAI(**conversation_data[c_key])
                            elif c_key == "lorebook" and isinstance(conversation_data[c_key], dict):
                                filtered_conversation[c_key] = ChatLorebookXoulAI(**conversation_data[c_key])
                            else:
                                filtered_conversation[c_key] = conversation_data[c_key]

                    filtered_data[key] = ChatConversationXoulAI(**filtered_conversation)

                elif key == "messages" and isinstance(data[key], list):
                    messages = []
                    for message in data[key]:
                        message_fields = {f.name for f in fields(ChatSingleMessageXoulAI)}
                        filtered_message = {}

                        for m_key in message:
                            if m_key in message_fields:
                                if m_key == "metadata" and isinstance(message[m_key], dict):
                                    metadata_fields = {f.name for f in fields(ChatMessageMetadataXoulAI)}
                                    filtered_metadata = {
                                        k: v for k, v in message[m_key].items() if k in metadata_fields
                                    }
                                    filtered_message[m_key] = ChatMessageMetadataXoulAI(**filtered_metadata)
                                else:
                                    filtered_message[m_key] = message[m_key]

                        messages.append(ChatSingleMessageXoulAI(**filtered_message))
                    filtered_data[key] = messages

                else:
                    filtered_data[key] = data[key]

        return cls(**filtered_data)
    
    def get_chat_description(self) -> list[str]:
        description = []

        if self.conversation:
            description.append(f"Character: {self.get_character_name()}")
            description.append(f"Personas: {', '.join(self.get_persona_names())}")
        else:
            description.append("ERROR: Conversation Data Missing")

        return description

    def get_character_name(self) -> str:
        if self.conversation and self.conversation.xouls:
            xoul = self.conversation.xouls[0]
            return xoul.name
        else:
            return "Unnamed Character"

    def get_character_slug(self) -> str:
        if self.conversation and self.conversation.xouls:
            xoul = self.conversation.xouls[0]
            return xoul.slug
        else:
            return "CHAR_ID_MISSING"
        
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
