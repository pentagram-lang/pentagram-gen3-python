from dataclasses import dataclass
from syntax_tree import Block
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class Value:
    pass


@dataclass
class ExpressionStack:
    values: List[Value]


@dataclass
class Environment:
    bindings: Dict[str, Value]
    link: Optional["Environment"]


@dataclass
class InstructionPointer:
    block: Block
    statement_index: int
    expression_term_index: int


@dataclass
class Frame:
    instruction_pointer: InstructionPointer
    expression_stack: ExpressionStack
    environment: Environment
    link: Optional["Frame"]
