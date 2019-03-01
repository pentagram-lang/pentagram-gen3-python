import sys

from environment import base_environment
from interpret import interpret
from loop import loop
from parse import parse_block
from parse import parse_statement
from stack_machine import ExpressionStack
from syntax_tree import Block


def main() -> None:
    if len(sys.argv) == 2:
        main_run(sys.argv[1])
    else:
        main_loop()


def main_run(source_filename: str) -> None:
    with open(source_filename, "r") as source_file:
        source_text = source_file.read()
    block = parse_block(source_text)
    expression_stack = ExpressionStack([])
    environment = base_environment()
    interpret(block, expression_stack, environment)
    if expression_stack.values:
        print(expression_stack.values)


def main_loop() -> None:
    environment = base_environment().extend({})

    def statement_loop(statement_text):
        statement = parse_statement(statement_text)
        block = Block([statement])
        expression_stack = ExpressionStack([])
        interpret(block, expression_stack, environment)
        return expression_stack.values

    loop(statement_loop)


if __name__ == "__main__":
    main()
