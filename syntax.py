from dataclasses import dataclass
from dataclasses import field
from numpy import integer
from typing import List
from typing import Optional
from typing import Type


@dataclass
class SyntaxTerm:
    pass


@dataclass
class SyntaxNumber(SyntaxTerm):
    value: integer
    value_type: Type = field(init=False)

    def __post_init__(self):
        self.value_type = type(self.value)
        assert issubclass(
            self.value_type, integer
        ), self.value_type


@dataclass
class SyntaxIdentifier(SyntaxTerm):
    name: str


@dataclass
class SyntaxComment(SyntaxTerm):
    text: str


@dataclass
class SyntaxBlock(SyntaxTerm):
    statements: List["SyntaxStatement"]


@dataclass
class SyntaxStatement:
    terms: List[SyntaxTerm]


@dataclass
class SyntaxExpression(SyntaxStatement):
    pass


@dataclass
class SyntaxBinding(SyntaxStatement):
    bindings: List[SyntaxIdentifier]


@dataclass
class SyntaxAssignment(SyntaxBinding):
    pass


@dataclass
class SyntaxModification(SyntaxBinding):
    pass
