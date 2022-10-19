from __future__ import annotations

from io import StringIO, BytesIO
from pathlib import Path

from ._types import FileData, FileType


def write_file(data: FileData, file: FileType, mode: str):
    if isinstance(file, str):
        file = Path(file)

    if isinstance(file, Path):
        if not file.parent.exists():
            raise ValueError(f"Can't find the directory '{file.parent}'")

        mode = f"{mode}b" if isinstance(data, bytes) else mode
        with open(file, mode) as f:
            f.write(data)
    elif isinstance(file, StringIO):
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        file.write(data)
    elif isinstance(file, BytesIO):
        if isinstance(data, str):
            data = data.encode("utf-8")
        file.write(data)
    else:
        raise ValueError(f"Wrong file type '{file}'")
