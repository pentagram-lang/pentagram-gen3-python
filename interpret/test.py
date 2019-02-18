from environment import base_environment
from interpret.interpret import init_frame_stack
from stack_machine import Environment
from stack_machine import ExpressionStack
from stack_machine import FrameStack
from syntax_tree import Block


def test_environment() -> Environment:
    return base_environment().extend({})


def init_test_frame_stack(
    block: Block, expression_stack: ExpressionStack
) -> FrameStack:
    return init_frame_stack(
        block, expression_stack, test_environment()
    )
