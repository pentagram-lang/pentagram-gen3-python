from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class Term:
    pass


@dataclass
class NumberTerm(Term):
    value: int


@dataclass
class IdentifierTerm(Term):
    name: str


@dataclass
class Comment:
    text: str


@dataclass
class Expression:
    terms: List[Term]
    comment: Optional[Comment]
    block: Optional["Block"]


@dataclass
class Statement:
    expression: Expression


@dataclass
class ExpressionStatement(Statement):
    pass


@dataclass
class AssignmentStatement(Statement):
    name: str


@dataclass
class ModificationStatement(Statement):
    name: str


@dataclass
class Block:
    statements: List[Statement]
