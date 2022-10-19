from __future__ import annotations

import subprocess as sp
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .file_operations import write_file
from ._types import FileType


@dataclass
class Command:
    value: str
    cwd: Path
    start: float
    end: float
    return_code: int
    result: None | sp.CalledProcessError | sp.CompletedProcess

    @property
    def stdout(self) -> str:
        if self.result is None:
            return ""
        else:
            return self.result.stdout.decode("utf-8")

    @property
    def stderr(self) -> str:
        if self.result is None:
            return ""
        else:
            return self.result.stderr.decode("utf-8")

    def __gt__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "w")
        return self.stdout

    def __rshift__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "a+")
        return self.stdout
