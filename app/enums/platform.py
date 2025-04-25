# enums/platform.py
from enum import Enum

class Platform(Enum):
    XOULAI = "XoulAI"
    # Add more as needed

    def __str__(self):
        return self.value  # Allows clean formatting when printed
