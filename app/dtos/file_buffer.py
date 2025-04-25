# dtos/file_buffer.py
from dataclasses import dataclass
from io import BytesIO

@dataclass
class FileBuffer:
    buffer: BytesIO
    filename: str
