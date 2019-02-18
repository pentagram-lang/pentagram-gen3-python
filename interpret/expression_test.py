from interpret.expression import interpret_expression
from interpret.test import init_test_frame_stack
from stack_machine import ExpressionStack
from stack_machine import FrameStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import NumberTerm


def init_expression_block(expression: Expression) -> Block:
    return Block([ExpressionStatement(expression)])


def test_interpret_expression_some():
    expression = Expression(
        [NumberTerm(100)], comment=None, block=None
    )
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_expression_block(expression), expression_stack
    )
    interpret_expression(frame_stack, expression)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack(
        [NumberValue(100)]
    )


def test_interpret_expression_none():
    expression = Expression([], comment=None, block=None)
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_expression_block(expression), expression_stack
    )
    interpret_expression(frame_stack, expression)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack([])
