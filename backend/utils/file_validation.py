from pathlib import Path
from typing import BinaryIO

from services.format_converter import SUPPORTED_EXTENSIONS

MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024


def validate_upload_file(file_obj: BinaryIO, filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Use PNG, JPG, JPEG, PDF, DXF, or DWG")

    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(0)
    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError("File exceeds 20MB limit")
