from ._types import FileType as FileType, PipeCmd as PipeCmd
from .command import Command as Command
from .file_operations import write_file as write_file
from .shell import Shell as Shell
from .utils import PipeExtractor as PipeExtractor
from .xargs import XArgs as XArgs, XArgsMeta as XArgsMeta
from typing import Any

class Pipe:
    sh: Shell
    stdout: Any
    stderr: Union[Any, None]
    return_code: int
    def __or__(self, cmd: Union[PipeCmd, PipeExtractor]) -> Union[Pipe, Any]: ...
    def __gt__(self, file: FileType) -> Any: ...
    def __rshift__(self, file: FileType) -> Any: ...
    def __init__(self, sh, stdout, stderr, return_code) -> None: ...
