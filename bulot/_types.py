from __future__ import annotations

from io import StringIO, BytesIO
from pathlib import Path
from typing import Union, TYPE_CHECKING

from . import PY


if TYPE_CHECKING:
    from .xargs import XArgs, XArgsMeta


class NotSet:
    pass


RunPipeCmd = Union[str, callable]
PipeCmd = Union[str, callable, "XArgs", "XArgsMeta"]
not_set = NotSet()

if PY >= "3.10":
    FileData = str | bytes
    FileType = str | Path | StringIO | BytesIO
else:
    FileData = Union[str, bytes]
    FileType = Union[str, Path, StringIO, BytesIO]
