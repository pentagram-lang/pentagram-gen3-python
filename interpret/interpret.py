from interpret.block import interpret_block
from stack_machine import Environment
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from stack_machine import InstructionPointer
from syntax_tree import Block


def interpret(block: Block, environment: Environment):
    frame_stack = FrameStack([])
    frame_stack.push(
        Frame(
            InstructionPointer(
                block,
                statement_index=0,
                expression_term_index=0
            ),
            ExpressionStack([]),
            environment,
        )
    )
    while frame_stack:
        interpret_block(frame_stack)
