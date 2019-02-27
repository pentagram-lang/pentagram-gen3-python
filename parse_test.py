import parsita

from numpy import int32
from parse import Parsers
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


def number_term_test():
    yield "123", NumberTerm(int32(123))
    yield "0xFF", NumberTerm(int32(255))
    yield "123.0", None


@params(number_term_test)
def test_number_term(text, expected_result):
    parse_test(Parsers.number_term, text, expected_result)


def identifier_term_test():
    yield "a-b-c", IdentifierTerm("a-b-c")


@params(identifier_term_test)
def test_identifier_term(text, expected_result):
    parse_test(
        Parsers.identifier_term, text, expected_result
    )


def expression_test():
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


@params(expression_test)
def test_expression(text, expected_result):
    parse_test(Parsers.expression, text, expected_result)


def block_test():
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


@params(block_test)
def test_block(text, expected_result):
    parse_test(Parsers.block, text, expected_result)
