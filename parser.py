import parsita

from syntax_tree import NumberTerm
from syntax_tree import IdentifierTerm
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import Block
from loop import loop


class Parsers(parsita.TextParsers, whitespace=None):
    number_term = parsita.reg(r"[0-9]+") > (
        lambda value: NumberTerm(int(value))
    )
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
