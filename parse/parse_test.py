import parsita

from numpy import int32
from numpy import int64
from numpy import uint8
from numpy import uint16
from numpy import uint32
from parse.parse import Parsers
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from test import params


def parse_test(parser, text, expected_result):
    result = parser.parse(text)
    if expected_result is not None:
        if hasattr(expected_result, "value_type"):
            print(expected_result.value_type)
        assert result.or_die() == expected_result
    else:
        assert isinstance(result, parsita.Failure)


def params_number_term():
    yield "123", NumberTerm(int32(123))
    yield "456d", NumberTerm(int64(456))
    yield "0xFF", NumberTerm(uint8(255))
    yield "0xF01D-AB1E", NumberTerm(uint32(0xF01DAB1E))
    yield "0x0h", NumberTerm(uint16(0))
    yield "0xab", None
    yield "123.0", None


@params(params_number_term)
def test_number_term(text, expected_result):
    parse_test(Parsers.number_term, text, expected_result)


def params_identifier_term():
    yield "a-b-c", IdentifierTerm("a-b-c")


@params(params_identifier_term)
def test_identifier_term(text, expected_result):
    parse_test(
        Parsers.identifier_term, text, expected_result
    )


def params_expression():
    yield "1 2 3", Expression(
        [
            NumberTerm(int32(1)),
            NumberTerm(int32(2)),
            NumberTerm(int32(3)),
        ],
        comment=None,
        block=None,
    )
    yield "abc d e", Expression(
        [
            IdentifierTerm("abc"),
            IdentifierTerm("d"),
            IdentifierTerm("e"),
        ],
        comment=None,
        block=None,
    )
    yield "123 abc", Expression(
        [NumberTerm(int32(123)), IdentifierTerm("abc")],
        comment=None,
        block=None,
    )


@params(params_expression)
def test_expression(text, expected_result):
    parse_test(Parsers.expression, text, expected_result)


def params_block():
    yield "123 abc\n456 def", Block(
        [
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(123)),
                        IdentifierTerm("abc"),
                    ],
                    comment=None,
                    block=None,
                )
            ),
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(int32(456)),
                        IdentifierTerm("def"),
                    ],
                    comment=None,
                    block=None,
                )
            ),
        ]
    )


@params(params_block)
def test_block(text, expected_result):
    parse_test(Parsers.block, text, expected_result)
