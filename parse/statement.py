from syntax_tree import AssignmentStatement
from syntax_tree import Block
from syntax_tree import Comment
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import Statement
from syntax_tree import Term
from typing import List
from typing import Optional


def parse_statement(
    terms: List[Term],
    comment: Optional[Comment],
    block: Optional[Block],
) -> Statement:
    bindings = []
    for term in terms:
        if isinstance(term, IdentifierTerm):
            if term.name == "=":
                return parse_assignment_statement(
                    bindings,
                    terms[len(bindings) + 1 :],
                    comment,
                    block,
                )
            else:
                bindings.append(term)
        else:
            break
    return parse_expression_statement(terms, comment, block)


def parse_expression_statement(
    terms: List[Term],
    comment: Optional[Comment],
    block: Optional[Block],
) -> ExpressionStatement:
    return ExpressionStatement(
        parse_expression(terms, comment, block)
    )


def parse_expression(
    terms: List[Term],
    comment: Optional[Comment],
    block: Optional[Block],
) -> Expression:
    return Expression(
        terms=terms, comment=comment, block=block
    )


def parse_assignment_statement(
    bindings: List[IdentifierTerm],
    terms: List[Term],
    comment: Optional[Comment],
    block: Optional[Block],
) -> AssignmentStatement:
    return AssignmentStatement(
        expression=parse_expression(terms, comment, block),
        bindings=bindings,
    )
