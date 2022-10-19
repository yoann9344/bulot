from __future__ import annotations

import re
import shlex
import subprocess as sp
import time
from collections.abc import Callable
from dataclasses import dataclass, asdict, field as data_field
from pathlib import Path
from typing import Any

from . import PY
from .aliases import Aliases
from .command import Command
from .logger import log
from .pipe import Pipe
from ._types import RunPipeCmd


@dataclass
class RunConfig:
    # run
    input: str | bytes | None
    capture_output: bool
    timeout: int | None
    check: bool
    # Popen
    bufsize: int
    executable: str | None
    stdin: int | None
    stdout: int | None
    stderr: int | None
    preexec_fn: callable | None
    close_fds: bool
    shell: bool  # to expand before runing (eg **/*.py, $HOME, ...)
    cwd: None  # use it to change directory
    env: None
    universal_newlines: None
    startupinfo: None
    creationflags: 0
    restore_signals: True
    start_new_session: False
    pass_fds: ()
    encoding: None
    errors: None
    text: None

    @classmethod
    def default(cls) -> "RunConfig":
        # fmt: off
        return cls(
            # run
            input=None, capture_output=True, timeout=None, check=False,
            # Popen
            bufsize=-1, executable=None, stdin=None, stdout=None,
            stderr=None, preexec_fn=None, close_fds=True, shell=False,
            cwd=None, env=None, universal_newlines=None, startupinfo=None,
            creationflags=0, restore_signals=True, start_new_session=False,
            pass_fds=(), encoding=None, errors=None, text=None,
        )
        # fmt: on


def do_nothing(*args, **kwargs):
    pass


@dataclass
class Shell:
    _cwd: Path = Path(__file__).parent
    fake: bool = False
    config: RunConfig = RunConfig.default()
    historic: list[Command] = data_field(default_factory=list)
    silent_piping: bool = True
    aliases = Aliases.default()

    def __post_init__(self, *args, **kwargs):
        self.config.cwd = str(self._cwd)

    def cd(self, path: Path | str):
        if isinstance(path, str):
            path = Path(path)

        if path.is_absolute:
            path = path.resolve()
        else:
            path = self.cd.joinpath(path).resolve()

        if not path.exists():
            raise sp.CalledProcessError(1, f"cd {str(path)}")

        self._cwd = path
        self.config.cwd = str(path)

    def cwd(self) -> Path:
        return self._cwd

    def run(
        self, cmd: str, *args, fake=False, callback=do_nothing, silent=False, **kwargs
    ) -> Command:
        command = Command(cmd, self._cwd, time.time(), -1.0, -1, None)
        self.historic.append(command)
        if silent:
            log.blabber(f"❯ {cmd}")
        else:
            log.info(f"❯ {cmd}")

        if self.fake or fake:
            command.return_code = 0
            command.end = command.start
            return

        if PY >= "3.9":
            config = asdict(self.config) | kwargs
        else:
            config = asdict(self.config)
            config.update(kwargs)
        cmd = self.aliases.process_aliases(cmd)

        cmd_args = shlex.split(cmd) + list(args)
        if config.get("shell", False):
            cmd_args = shlex.split(cmd) + list(args)

        try:
            completed_process: sp.CompletedProcess = sp.run(cmd_args, **config)
            result = completed_process
        except sp.CalledProcessError as exc:
            result = exc
            raise exc
        finally:
            command.return_code = result.returncode
            command.result = result
            command.end = time.time()

            if silent:
                log.blabber(command.stdout, end="")
            else:
                log.info(command.stdout, end="")

            log.error(command.stderr, end="")
            callback(command=command)
        return command

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __or__(self, cmd: RunPipeCmd) -> "Pipe":
        stdout = self.run_pipe(cmd)
        return Pipe(sh=self, stdout=stdout)

    def __lshift__(self, stdin: Any) -> "Pipe":
        return Pipe(sh=self, stdout=stdin)

    def run_pipe(self, cmd: RunPipeCmd, **kwargs) -> Any:
        if isinstance(cmd, str):
            if isinstance(kwargs.get("input"), str):
                kwargs["input"] = kwargs["input"].encode("utf-8")
            stdout = self.run(
                cmd, silent=self.silent_piping, check=True, **kwargs
            ).stdout
        elif isinstance(cmd, Callable):
            stdin = kwargs.get("input")
            if stdin is not None:
                stdout = cmd(stdin)
            else:
                stdout = cmd()
        else:
            raise NotImplementedError("Shell does not support type {type(cmd)}.")

        return stdout
