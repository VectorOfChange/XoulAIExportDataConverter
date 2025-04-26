# enums/bug_type.py
from enum import Enum

class BugType(Enum):
    APP = "App"
    DATA = "Data"

    def __str__(self):
        return self.value  # Allows clean formatting when printed
