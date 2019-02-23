from host.simple_call import sqrt
from interpret import interpret
from interpret.test import test_environment
from stack_machine import ExpressionStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm


def call_test(binding, args, results):
    term = IdentifierTerm(sqrt.name)
    block = Block(
        [
            ExpressionStatement(
                Expression([term], comment=None, block=None)
            )
        ]
    )
    expression_stack = ExpressionStack(args)
    environment = test_environment()
    interpret(block, expression_stack, environment)
    assert expression_stack == ExpressionStack(results)


def test_sqrt():
    call_test(sqrt, [NumberValue(4)], [NumberValue(2)])
