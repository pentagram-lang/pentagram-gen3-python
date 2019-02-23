import parsita

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
        assert result.or_die() == expected_result
    else:
        assert isinstance(result, parsita.Failure)


def number_term_test():
    yield "123", NumberTerm(123)
    yield "0xFF", NumberTerm(255)
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
        [NumberTerm(1), NumberTerm(2), NumberTerm(3)],
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
        [NumberTerm(123), IdentifierTerm("abc")],
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
                        NumberTerm(123),
                        IdentifierTerm("abc"),
                    ],
                    comment=None,
                    block=None,
                )
            ),
            ExpressionStatement(
                Expression(
                    [
                        NumberTerm(456),
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
