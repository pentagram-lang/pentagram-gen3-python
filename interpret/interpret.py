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
):
    frame_stack = init_frame_stack(
        block, expression_stack, environment
    )
    while frame_stack:
        interpret_block(frame_stack)


def init_frame_stack(
    block: Block,
    expression_stack: ExpressionStack,
    environment: Environment,
) -> FrameStack:
    return FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=0,
                ),
                expression_stack,
                environment,
            )
        ]
    )
