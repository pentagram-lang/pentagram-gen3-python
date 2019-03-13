from interpret.block import interpret_block
from stack_machine import Environment
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from stack_machine import InstructionPointer
from syntax_tree import Block


def interpret(
    block: Block,
    expression_stack: ExpressionStack,
    environment: Environment,
) -> None:
    frame_stack = init_frame_stack(
        block, expression_stack, environment
    )
    while frame_stack:
        interpret_block(frame_stack)


def init_frame_stack(
    block: Block,
    expression_stack: ExpressionStack,
    environment: Environment,
    statement_index: int = 0,
    expression_term_index: int = 0,
) -> FrameStack:
    return FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index,
                    expression_term_index,
                ),
                expression_stack,
                environment,
            )
        ]
    )
