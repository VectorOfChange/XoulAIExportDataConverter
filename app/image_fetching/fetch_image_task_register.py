# image_fetching/fetch_image_task_register.py
from os import path
from typing import Optional
from dtos.fetch_image_task import FetchImageTask
from globals.globals import IMAGES_FOLDER_PATH

class FetchImageTaskRegister:
    def __init__(self):
        self._tasks_by_url: dict[str, FetchImageTask] = {}
        self._serial_counter = 1  # start numbering at 1

    def registerNewTask(self, url: str, file_description: str) -> Optional[FetchImageTask]:
        if not url:
            # TODO: add error management here
            return None

        # TODO: fix this at model level
        if isinstance(url, list):
            safe_url = url[0]
        else:
            safe_url = url

        if safe_url in self._tasks_by_url:
            # Already registered, return existing task
            return self._tasks_by_url[safe_url]
        
        # Extract file extension from URL
        file_extension = self._get_file_extension(safe_url)
        
        # Not registered: generate unique filename
        serial = self._serial_counter
        file_name = f"IMG_{serial:04d}_{file_description}{file_extension}"
        file_path = IMAGES_FOLDER_PATH + file_name
        
        task = FetchImageTask(url=safe_url, file_path=file_path, file_name=file_name)
        self._tasks_by_url[safe_url] = task
        self._serial_counter += 1

        return task
    
    def _get_file_extension(self, url: str) -> str:
        # Extract file extension from the URL
        _, ext = path.splitext(url)
        
        # Ensure it has an extension, default to '.jpg' if missing
        return ext if ext else '.jpg'

    def get_tasks(self) -> list[FetchImageTask]:
        return list(self._tasks_by_url.values())