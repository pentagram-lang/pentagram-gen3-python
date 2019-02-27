import parsita

from loop import loop
from numpy import int32
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from syntax_tree import Statement


class Parsers(parsita.TextParsers, whitespace=None):
    decimal_number_term = parsita.reg(r"[0-9]+") > (
        lambda value: int32(value)
    )
    hex_number_term = (
        parsita.lit("0x") >> parsita.reg(r"[0-9A-Fa-f]+")
    ) > (lambda value: int32(int(value, base=16)))
    number_term = (
        hex_number_term | decimal_number_term
    ) > NumberTerm
    identifier_term = (
        parsita.reg(r"[\S^\d]\S*") > IdentifierTerm
    )
    term = number_term | identifier_term
    space = parsita.reg(r" +")
    expression = parsita.repsep(term, space) > (
        lambda terms: Expression(
            terms, comment=None, block=None
        )
    )
    expression_statement = expression > ExpressionStatement
    statement = expression_statement
    block = parsita.repsep(statement, "\n") > Block


def parse_statement(text: str) -> Statement:
    return Parsers.statement.parse(text).or_die()


def parse_block(text: str) -> Block:
    return Parsers.block.parse(text).or_die()


if __name__ == "__main__":
    loop(Parsers.statement.parse)
