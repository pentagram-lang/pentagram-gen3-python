#!/usr/bin/env python
import sys

from environment import base_environment
from interpret import interpret
from loop import loop
from parse import Parsers
from stack_machine import Environment
from stack_machine import ExpressionStack
from syntax_tree import Block
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
    environment: Optional[Environment] = None,
) -> None:
    with open(source_filename, "r") as source_file:
        source_text = source_file.read()
    block = Parsers.block.parse(source_text).or_die()
    expression_stack = ExpressionStack([])
    if not environment:
        environment = base_environment()
    interpret(block, expression_stack, environment)
    if expression_stack.values:
        print(expression_stack.values)


def main_loop() -> None:
    environment = base_environment().extend({})

    def statement_loop(statement_text):
        statement = Parsers.statement.parse(
            statement_text
        ).or_die()
        block = Block([statement])
        expression_stack = ExpressionStack([])
        interpret(block, expression_stack, environment)
        return expression_stack.values

    loop(statement_loop)


def parse_loop() -> None:
    loop(Parsers.statement.parse)


if __name__ == "__main__":
    main()
