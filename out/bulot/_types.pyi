from .xargs import XArgs as XArgs, XArgsMeta as XArgsMeta
from _typeshed import Incomplete
from io import BytesIO, StringIO
from pathlib import Path
from typing import Callable, Union

class NotSet: ...
RunPipeCmd = Union[str, Callable]
PipeCmd: Incomplete
not_set: Incomplete
FileData = Union[str, bytes]
FileType = Union[str, Path, StringIO, BytesIO]
