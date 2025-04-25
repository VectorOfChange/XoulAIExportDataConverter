# enums/type_group.py
from enum import Enum

class TypeGroup(Enum):
    CHAT = "Chat History"
    NONCHAT = "Data Other Than Chat History"

    def __str__(self):
        return self.value  # Allows clean formatting when printed
