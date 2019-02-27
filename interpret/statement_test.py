import interpret.statement

from interpret.test import init_test_frame_stack
from numpy import int32
from stack_machine import ExpressionStack
from stack_machine import FrameStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import NumberTerm
from syntax_tree import Statement

interpret_expression_statement = (
    interpret.statement.interpret_expression_statement
)


def init_statement_block(statement: Statement) -> Block:
    return Block([statement])


def test_interpret_expression_statement():
    statement = ExpressionStatement(
        Expression(
            [NumberTerm(int32(100))],
            comment=None,
            block=None,
        )
    )
    expression_stack = ExpressionStack([])
    frame_stack = init_test_frame_stack(
        init_statement_block(statement), expression_stack
    )
    interpret_expression_statement(frame_stack, statement)
    assert frame_stack == FrameStack([])
    assert expression_stack == ExpressionStack(
        [NumberValue(int32(100))]
    )
