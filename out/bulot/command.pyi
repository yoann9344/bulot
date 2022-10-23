import subprocess as sp
from ._types import FileType as FileType
from .file_operations import write_file as write_file
from pathlib import Path
from typing import Any

class Command:
    value: str
    cwd: Path
    start: float
    end: float
    return_code: int
    result: Union[None, sp.CalledProcessError, sp.CompletedProcess]
    fake: bool
    @property
    def stdout(self) -> str: ...
    @property
    def stderr(self) -> str: ...
    def __gt__(self, file: FileType) -> Any: ...
    def __rshift__(self, file: FileType) -> Any: ...
    def __init__(self, value, cwd, start, end, return_code, result, fake) -> None: ...
