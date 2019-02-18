import sys

from environment import base_environment
from interpret import interpret
from interpret.block import interpret_block
from loop import loop
from parse import parse_block
from parse import parse_statement
from stack_machine import Environment
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from stack_machine import InstructionPointer
from syntax_tree import Block


def main():
    if len(sys.argv) == 2:
        main_run(sys.argv[1])
    else:
        main_loop()


def main_run(source_filename):
    with open(source_filename, "r") as source_file:
        source_text = source_file.read()
    block = parse_block(source_text)
    environment = base_environment()
    interpret(block, environment)


def main_loop():
    environment = Environment(dict(), base_environment())
    block = Block([])

    def statement_loop(statement_text):
        statement = parse_statement(statement_text)
        block.statements.append(statement)
        expression_stack = ExpressionStack([])
        frame_stack = FrameStack([])
        frame_stack.push(
            Frame(
                InstructionPointer(
                    block,
                    statement_index=len(block.statements)
                    - 1,
                    expression_term_index=0,
                ),
                expression_stack,
                environment,
            )
        )
        while frame_stack:
            interpret_block(frame_stack)
        return expression_stack.values

    loop(statement_loop)


if __name__ == "__main__":
    main()
