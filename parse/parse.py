import parsita

from loop import loop
from parse.parse_number import parse_number
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from syntax_tree import Statement


def hyphen_sequence_complex(
    head: str, body: str
) -> parsita.Parser[str, str]:
    return parsita.reg(
        rf"(?!-){head}(?:-?(?:(?!-){body})+)*"
    )


def hyphen_sequence_simple(
    body: str
) -> parsita.Parser[str, str]:
    return hyphen_sequence_complex(body, body)


def opt_default(
    parser: parsita.Parser[str, str], default
) -> parsita.Parser[str, str]:
    return parsita.opt(parser) > (
        lambda result_list: result_list[0]
        if result_list
        else default
    )


class Parsers(parsita.TextParsers, whitespace=None):
    number_term_suffix = parsita.reg(r"[iuf]?[bhwd]?")
    decimal_number_term = hyphen_sequence_simple(
        r"[0-9]"
    ) & number_term_suffix > (
        lambda digits_and_suffix: parse_number(
            10, *digits_and_suffix
        )
    )
    hex_number_term = (
        parsita.lit("0x")
        >> hyphen_sequence_simple(r"[0-9A-F]+")
        & opt_default(
            parsita.lit("x") >> number_term_suffix, ""
        )
    ) > (
        lambda digits_and_suffix: parse_number(
            16, *digits_and_suffix
        )
    )
    number_term = (
        hex_number_term | decimal_number_term
    ) > NumberTerm
    identifier_term = (
        hyphen_sequence_complex(r"(?!\d)\S", r"\S")
        > IdentifierTerm
    )
    term = number_term | identifier_term
    space = parsita.reg(r" +")
    expression = parsita.repsep(term, space) << parsita.opt(
        space
    ) & (
        opt_default(
            parsita.lit("--") >> parsita.reg(r"[^\n]*"),
            None,
        )
    ) > (
        lambda terms_and_comment: Expression(
            *terms_and_comment, block=None
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
