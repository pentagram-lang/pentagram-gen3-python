from numpy import int32
from parse.statement import parse_statement
from syntax_tree import AssignmentStatement
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from test import params


def params_statement():
    yield [], ExpressionStatement(
        expression=Expression([], comment=None, block=None)
    )
    yield [
        NumberTerm(int32(1)),
        NumberTerm(int32(2)),
        IdentifierTerm("*"),
    ], ExpressionStatement(
        expression=Expression(
            [
                NumberTerm(int32(1)),
                NumberTerm(int32(2)),
                IdentifierTerm("*"),
            ],
            comment=None,
            block=None,
        )
    )
    yield [
        IdentifierTerm("x"),
        IdentifierTerm("="),
        NumberTerm(int32(1)),
    ], AssignmentStatement(
        expression=Expression(
            [NumberTerm(int32(1))], comment=None, block=None
        ),
        bindings=[IdentifierTerm("x")],
    )
    yield [
        IdentifierTerm("x"),
        IdentifierTerm("y"),
        IdentifierTerm("z"),
        IdentifierTerm("="),
        IdentifierTerm("three"),
    ], AssignmentStatement(
        expression=Expression(
            [IdentifierTerm("three")],
            comment=None,
            block=None,
        ),
        bindings=[
            IdentifierTerm("x"),
            IdentifierTerm("y"),
            IdentifierTerm("z"),
        ],
    )


@params(params_statement)
def test_statement(terms, expected_result):
    assert (
        parse_statement(terms, comment=None, block=None)
        == expected_result
    )
