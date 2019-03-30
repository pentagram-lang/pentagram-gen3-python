#!/usr/bin/env python
import sys

from environment import base_environment
from interpret import interpret
from loop import loop
from machine import MachineEnvironment
from machine import MachineExpressionStack
from parse import parse
from typing import Optional


def main() -> None:
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == "--parse":
            parse_loop()
        else:
            main_run(arg)
    else:
        main_loop()


def main_run(
    source_filename: str,
    environment: Optional[MachineEnvironment] = None,
) -> None:
    with open(source_filename, "r") as source_file:
        source_text = source_file.read()
    block = parse(source_text)
    expression_stack = MachineExpressionStack([])
    if not environment:
        environment = base_environment()
    interpret(block, expression_stack, environment)
    if expression_stack.values:
        print(expression_stack.values)


def main_loop() -> None:
    environment = base_environment().extend()

    def statement_loop(statement_text):
        block = parse(statement_text)
        expression_stack = MachineExpressionStack([])
        interpret(block, expression_stack, environment)
        return expression_stack.values

    loop(statement_loop)


def parse_loop() -> None:
    loop(parse)


if __name__ == "__main__":
    main()
