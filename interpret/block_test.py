from interpret.block import interpret_block
from interpret.test import init_test_frame_stack
from numpy import int32
from stack_machine import ExpressionStack
from stack_machine import FrameStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import NumberTerm


def test_interpret_block_enter():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [NumberTerm(int32(4))],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    frame_stack = init_test_frame_stack(
        block, ExpressionStack([])
    )
    interpret_block(frame_stack)
    assert frame_stack == init_test_frame_stack(
        block,
        ExpressionStack([NumberValue(int32(4))]),
        expression_term_index=1,
    )


def test_interpret_block_exit():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [NumberTerm(int32(4))],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    frame_stack = init_test_frame_stack(
        block, ExpressionStack([]), statement_index=1
    )
    interpret_block(frame_stack)
    assert frame_stack == FrameStack([])
