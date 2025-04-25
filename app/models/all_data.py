# models/all_data.py
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AllData:
    _data_list: List[Dict[str, Any]] = field(init=False)

    def __init__(self, data_xoulai: Dict[str, Any]):
        self._data_list = [data_xoulai]

    def add_platform_data(self, new_data: Dict[str, Any]) -> None:
        """Add platform-specific data to the list."""
        self._data_list.append(new_data)

    def get_xoulai_data(self) -> Dict[str, Any]:
        """Return the original XoulAI Data (first element)."""
        return self._data_list[0]

    def get_all_data(self) -> List[Dict[str, Any]]:
        """Return the full list of all data."""
        return self._data_list
