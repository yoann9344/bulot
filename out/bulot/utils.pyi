from .pipe import Pipe as Pipe
from _typeshed import Incomplete
from typing import Any

class PipeExtractor:
    attr: str
    def __call__(self, pipe: Pipe) -> Any: ...

class Stdout(PipeExtractor):
    attr: str

class Stderr(PipeExtractor):
    attr: str

class Stdin(PipeExtractor):
    attr: str

stdout: Incomplete
stderr: Incomplete
stdin: Incomplete
