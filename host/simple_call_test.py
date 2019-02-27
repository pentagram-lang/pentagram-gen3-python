from host.simple_call import add
from host.simple_call import nil_blob
from host.simple_call import sqrt
from interpret import interpret
from interpret.test import test_environment
from numpy import int32
from stack_machine import BlobValue
from stack_machine import ExpressionStack
from stack_machine import NumberValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm


def call_test(binding, args, results):
    term = IdentifierTerm(binding.name)
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


def test_add_blob():
    call_test(
        add,
        [
            BlobValue(bytearray()),
            NumberValue(int32(0x1234_5678)),
        ],
        [BlobValue(bytearray(b"\x78\x56\x34\x12"))],
    )


def test_nil_blob():
    call_test(nil_blob, [], [BlobValue(bytearray())])


def test_sqrt():
    call_test(
        sqrt,
        [NumberValue(int32(4))],
        [NumberValue(int32(2))],
    )
