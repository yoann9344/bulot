# Bulot
Helper to run Bash commands with python

[![PyPI - Version](https://img.shields.io/pypi/v/bulot.svg)](https://pypi.org/project/bulot)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bulot.svg)](https://pypi.org/project/bulot)

-----

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)
    - [Concept](#concept)
    - [Classes](#classes)
    - [Git](#git)
- [License](#license)

## Installation

```console
pip install bulot
```

## Examples

### Concept
```python
from bulot import Shell

# Create a shell
sh = Shell()
sh | "ls" | print

# Create another shell independant from the first one
sh2 = Shell()
sh2.cd("..")
print(sh2.cwd())
# remove alias for ls
del sh2.aliases["ls"]
files = sh2 | "ls"
# without the alias, will print ls without color
print(files)
```

### Classes
```python
import json
import re
from bulot import xargs
from pprint import pprint
from glob import glob


def jprint(data):
    print(json.dumps(data, indent=4))


def extract_classes(stdin: str) -> list:
    """Returns classes' name"""
    def extract_name(class_line):
        return re.sub(r"class (\w+).*:", r"\1", class_line)

    return [extract_name(line) for line in stdin.splitlines() if line.startswith("class")]


# `sh | "ls *.py"` can't expand * then we must use glob
# see https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
classes = sh << glob("bulot/*.py") | xargs - "cat {}" | "\n".join | extract_classes
classes | print
classes | pprint
classes | jprint
assert "Shell" in classes.stdout

```

## License

`Bulot` is distributed under the terms of the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) license.

