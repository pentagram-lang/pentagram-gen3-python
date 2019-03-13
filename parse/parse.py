import parsita

from parse.number import parse_number
from parse.statement import parse_statement
from syntax_tree import Block
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm


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
    statement = parsita.repsep(term, space) << parsita.opt(
        space
    ) & (
        opt_default(
            parsita.lit("--") >> parsita.reg(r"[^\n]*"),
            None,
        )
    ) > (
        lambda terms_and_comment: parse_statement(
            *terms_and_comment, block=None
        )
    )
    block = parsita.repsep(statement, "\n") > Block
