from environment import base_environment
from interpret.interpret import init_frame_stack
from stack_machine import Call
from stack_machine import Environment
from stack_machine import ExpressionStack
from stack_machine import FrameStack
from stack_machine import Value
from syntax_tree import Block
from typing import Dict
from typing import Optional
from typing import Union


def test_environment(
    bindings: Optional[Dict[str, Union[Value, Call]]] = None
) -> Environment:
    return base_environment().extend(bindings or {})


def init_test_frame_stack(
    block: Block,
    expression_stack: ExpressionStack,
    statement_index: int = 0,
    expression_term_index: int = 0,
) -> FrameStack:
    return init_frame_stack(
        block=block,
        expression_stack=expression_stack,
        environment=test_environment(),
        statement_index=statement_index,
        expression_term_index=expression_term_index,
    )
