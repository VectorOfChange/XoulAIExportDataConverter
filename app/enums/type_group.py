# enums/type_group.py
from enum import Enum

class TypeGroup(Enum):
    CHAT = "Chat Transcript"
    NONCHAT = "Data Other Than Chat Transcripts"

    def __str__(self):
        return self.value  # Allows clean formatting when printed
