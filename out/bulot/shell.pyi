from ._py_version import PY as PY
from ._types import RunPipeCmd as RunPipeCmd
from .aliases import Aliases as Aliases
from .command import Command as Command
from .logger import log as log
from .pipe import Pipe as Pipe
from _typeshed import Incomplete
from pathlib import Path
from typing import Any, Callable

class RunConfig:
    input: Union[str, bytes, None]
    capture_output: bool
    timeout: Union[int, None]
    check: bool
    bufsize: int
    executable: Union[str, None]
    stdin: Union[int, None]
    stdout: Union[int, None]
    stderr: Union[int, None]
    preexec_fn: Union[Callable, None]
    close_fds: bool
    shell: bool
    cwd: Union[str, None]
    env: Union[dict, None]
    universal_newlines: None
    startupinfo: None
    creationflags: int
    restore_signals: bool
    start_new_session: bool
    pass_fds: tuple
    encoding: None
    errors: None
    text: None
    @classmethod
    def default(cls) -> RunConfig: ...
    def __init__(self, input, capture_output, timeout, check, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, encoding, errors, text) -> None: ...

def do_nothing(*args, **kwargs) -> None: ...

class Shell:
    fake: bool
    config: RunConfig
    historic: list[Command]
    silent_piping: bool
    aliases: Incomplete
    def __post_init__(self, *args, **kwargs) -> None: ...
    def cd(self, path: Union[Path, str]): ...
    def cwd(self) -> Path: ...
    def run(self, cmd: str, *args, fake: bool = ..., callback=..., silent: bool = ..., **kwargs) -> Command: ...
    def __call__(self, *args, **kwargs): ...
    def __or__(self, cmd: RunPipeCmd) -> Pipe: ...
    def __lshift__(self, stdin: Any) -> Pipe: ...
    def run_pipe(self, cmd: RunPipeCmd, **kwargs) -> Union[Any, Command]: ...
    def __init__(self, _cwd, fake, config, historic, silent_piping) -> None: ...
