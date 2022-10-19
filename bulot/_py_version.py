import sys


def cmp(a, b):
    return (a > b) - (a < b)


class PythonVersion:
    version = sys.version_info[:3]

    def compare(self, expected: str) -> int:
        expected = list(map(int, expected.split(".")))
        print(expected)

        for exp, ver in zip(expected, self.version):
            comparaison = cmp(ver, exp)
            if comparaison != 0:
                return comparaison

        return 0

    def __eq__(self, expected: str) -> bool:
        return self.compare(expected) == 0

    def __lt__(self, expected: str) -> bool:
        return self.compare(expected) < 0

    def __le__(self, expected: str) -> bool:
        return self.compare(expected) <= 0

    def __gt__(self, expected: str) -> bool:
        return self.compare(expected) > 0

    def __ge__(self, expected: str) -> bool:
        return self.compare(expected) >= 0


PY = PythonVersion()
