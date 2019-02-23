from interpret.block import interpret_block
from interpret.test import test_environment
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from stack_machine import InstructionPointer
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import NumberTerm


def test_interpret_block():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [NumberTerm(4)],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    expression_stack = ExpressionStack([])
    frame_stack = FrameStack(
        [
            Frame(
                InstructionPointer(
                    block,
                    statement_index=0,
                    expression_term_index=0,
                ),
                expression_stack,
                test_environment(),
            )
        ]
    )
    interpret_block(frame_stack)
    expected_frame_stack = FrameStack([])
    assert frame_stack == expected_frame_stack
    assert expression_stack == ExpressionStack(
        [NumberValue(4)]
    )
