# models/all_data.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

from models.platform_xoulai.all_data_xoulai import AllDataXoulAI


@dataclass
class AllData:
    _platform_data_list: List[Any] = field(init=False)

    def __init__(self, data_xoulai: AllDataXoulAI):
        self._platform_data_list = [data_xoulai]

    def add_platform_data(self, new_data: Any) -> None:
        """Add platform-specific data to the list."""
        self._platform_data_list.append(new_data)

    def get_xoulai_platform_data(self) -> AllDataXoulAI:
        """Return the original XoulAI Data (first element)."""
        return self._platform_data_list[0]

    def get_all_platform_data(self) -> List[Any]:
        """Return the full list of all data."""
        return self._platform_data_list
