# image_fetching/fetch_images.py
import time
import streamlit as st
import requests
from io import BytesIO

from dtos.file_buffer import FileBuffer
from image_fetching.fetch_image_task_register import FetchImageTaskRegister
from utils.custom_logger import log

def download_image(url, retries=1, delay=1):
    """Attempts to download an image, retrying once if it fails."""
    for attempt in range(retries + 1):  # first try + retries
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # raises HTTPError for bad status
            return BytesIO(response.content)
        except Exception as e:
            # TODO: better log message, track failed files
            log(f"Failed to download image from {url} (attempt {attempt + 1} of {retries}): {e}")
            if attempt < retries:
                time.sleep(delay)  # wait before retry
    return None  # failed after retries

def fetch_images(on_progress=None) -> list[FileBuffer]:
    image_buffers: list[FileBuffer] = []
    
    register: FetchImageTaskRegister = st.session_state.fetch_image_task_register
    fetch_image_tasks = register.get_tasks()
    total_tasks = len(fetch_image_tasks)

    for idx, task in enumerate(fetch_image_tasks):
        if task.url: # skip if null/None
            image_buffer = download_image(task.url, retries=1, delay=1)
            if image_buffer:
                image_buffers.append(FileBuffer(image_buffer, task.file_path))
                time.sleep(1) # wait to prevent hammering of Xoul servers
            else:
                log(f"Skipping image file {task.file_path} due to failed download.")
        if on_progress:
            on_progress(idx + 1, total_tasks) # add one to compensate for zero-indexed index value

    return image_buffers