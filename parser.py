import parsita

from dataclasses import dataclass


@dataclass
class Number:
    value: int


@dataclass
class Identifier:
    name: str


class Parsers(parsita.TextParsers, whitespace=None):
    number = parsita.reg(r"[0-9]+") > (
        lambda value: Number(int(value))
    )
    identifier = parsita.reg(r"[\S^\d]\S*") > Identifier
    token = number | identifier
    space = parsita.reg(r" +")
    line = parsita.repsep(token, space)
    lines = parsita.repsep(line, "\n")


if __name__ == "__main__":
    try:
        while True:
            text = input("> ")
            print(Parsers.line.parse(text), "\n")
    except KeyboardInterrupt:
        pass
