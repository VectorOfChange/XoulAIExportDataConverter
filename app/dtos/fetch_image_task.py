# dtos/fetch_image_task.py
from dataclasses import dataclass

@dataclass
class FetchImageTask:
    url: str
    file_path: str
    file_name: str