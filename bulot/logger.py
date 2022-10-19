from enum import Enum, IntEnum
from functools import partialmethod


class Level(IntEnum):
    blabber = 0
    debug = 1
    info = 2
    warning = 3
    error = 4
    critical = 5


class LevelColor(Enum):
    blabber = 0
    debug = 1
    info = 2
    warning = 3
    error = 4
    critical = 5


class Logger:
    level = Level.info

    def _print(self, *args, level=Level, **kwargs):
        if level.value >= self.level.value:
            print(*args, **kwargs)

    @classmethod
    def _add_level(cls, level: Level):
        def print_level(self, *args, level=Level, **kwargs):
            self._print(*args, level=level, **kwargs)

        method = partialmethod(print_level, level=level)
        # method.__doc__ = ""
        method.__name__ = level.name
        setattr(cls, method.__name__, method)


for level in Level.__members__.values():
    Logger._add_level(level)


# main loggger
log = Logger()


if __name__ == "__main__":
    log.debug("debug")
    log.info("info")
    log.info("warning")
