from interpret import interpret
from interpret.test import test_environment
from numpy import int32
from stack_machine import ExpressionStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import NumberTerm


def test_interpret():
    block = Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(1)),
                        NumberTerm(int32(2)),
                        NumberTerm(int32(3)),
                    ],
                    comment=None,
                    block=None,
                )
            )
        ]
    )
    expression_stack = ExpressionStack([])
    environment = test_environment()
    interpret(block, expression_stack, environment)
    assert expression_stack == ExpressionStack(
        [
            NumberValue(int32(1)),
            NumberValue(int32(2)),
            NumberValue(int32(3)),
        ]
    )
