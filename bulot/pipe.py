from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING


from .file_operations import write_file
from .xargs import XArgs, XArgsMeta
from ._types import PipeCmd, FileType

if TYPE_CHECKING:
    from .shell import Shell


@dataclass
class Pipe:
    sh: Shell
    stdout: Any

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(stdout={repr(self.stdout)})"

    def __or__(self, cmd: PipeCmd) -> "Pipe":
        stdin = self.stdout
        if isinstance(cmd, XArgsMeta):
            stdout = cmd(stdin=stdin)
        elif isinstance(stdin, XArgs):
            stdout = stdin.run(cmd, shell=self.sh)
        elif isinstance(cmd, XArgs):
            cmd = cmd(stdin=stdin)
            stdout = cmd.run(stdin, shell=self.sh)
        else:
            stdout = self.sh.run_pipe(cmd, input=stdin)

        return Pipe(sh=self.sh, stdout=stdout)

    def __gt__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "w")
        return self.stdout

    def __rshift__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "a+")
        return self.stdout
