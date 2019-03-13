from dataclasses import dataclass
from dataclasses import field
from numpy import integer
from typing import List
from typing import Optional
from typing import Type


@dataclass
class Term:
    pass


@dataclass
class NumberTerm(Term):
    value: integer
    value_type: Type = field(init=False)

    def __post_init__(self):
        self.value_type = type(self.value)
        assert issubclass(
            self.value_type, integer
        ), self.value_type


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
    bindings: List[IdentifierTerm]


@dataclass
class ModificationStatement(Statement):
    bindings: List[IdentifierTerm]


@dataclass
class Block:
    statements: List[Statement]
