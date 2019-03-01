from host.simple_call import add
from host.simple_call import nil_blob
from host.simple_call import sqrt
from host.simple_call import write
from interpret import interpret
from interpret.test import test_environment
from io import BytesIO
from numpy import int16
from numpy import int32
from numpy import uint8
from numpy import uint64
from stack_machine import BlobValue
from stack_machine import ExpressionStack
from stack_machine import NumberValue
from stack_machine import StreamValue
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from test import params


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


def params_add_blob():
    yield uint8(0xF7), b"\xF7"
    yield int16(0xABCD), b"\xCD\xAB"
    yield int32(0x1234_5678), b"\x78\x56\x34\x12"
    yield uint64(1), b"\x01\0\0\0\0\0\0\0"


@params(params_add_blob)
def test_add_blob(number, expected):
    call_test(
        add,
        [BlobValue(bytearray()), NumberValue(number)],
        [BlobValue(bytearray(expected))],
    )


def test_nil_blob():
    call_test(nil_blob, [], [BlobValue(bytearray())])


def test_sqrt():
    call_test(
        sqrt,
        [NumberValue(int32(4))],
        [NumberValue(int32(2))],
    )


def test_write():
    bytes_io = BytesIO()
    call_test(
        write,
        [
            StreamValue(bytes_io),
            BlobValue(bytearray(b"abcdef")),
        ],
        [],
    )
    assert bytes_io.getvalue() == b"abcdef"
