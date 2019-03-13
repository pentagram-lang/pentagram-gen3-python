from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from io import IOBase
from numpy import integer
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import Statement
from syntax_tree import Term
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class Value:
    pass


@dataclass
class BlobValue(Value):
    value: bytearray


@dataclass
class NumberValue(Value):
    value: integer
    value_type: Type = field(init=False)

    def __post_init__(self):
        self.value_type = type(self.value)
        assert issubclass(
            self.value_type, integer
        ), self.value_type


@dataclass
class StreamValue(Value):
    value: IOBase


@dataclass
class ExpressionStack:
    values: List[Value]

    def push(self, value: Value) -> None:
        self.values.append(value)

    def push_many(self, values: List[Value]) -> None:
        for value in values:
            self.push(value)

    def pop(self) -> Value:
        return self.values.pop()

    def pop_many(self, count: int) -> Value:
        assert len(self) >= count
        values = []
        for _ in range(count):
            values.append(self.values.pop())
        return values

    def __len__(self) -> int:
        return len(self.values)


@dataclass
class Call(ABC):
    @abstractmethod
    def __call__(self, frame_stack: "FrameStack") -> None:
        pass


@dataclass
class Binding:
    name: str
    value_or_call: Union[Value, Call]

    @property
    def value(self):
        assert isinstance(self.value_or_call, Value)
        return self.value_or_call

    @property
    def call(self):
        assert isinstance(self.value_or_call, Call)
        return self.value_or_call


@dataclass
class Environment:
    bindings: Dict[str, Union[Value, Call]]
    base: Optional["Environment"]

    def extend(
        self, bindings: Dict[str, Union[Value, Call]]
    ) -> "Environment":
        return Environment(bindings, base=self)

    def __getitem__(self, key: str) -> Union[Value, Call]:
        value = self.bindings.get(key)
        if value is None:
            if self.base:
                return self.base[key]
            else:
                raise KeyError(key)
        else:
            return value

    def __setitem__(
        self, key: str, value: Union[Value, Call]
    ) -> None:
        self.bindings[key] = value

    def from_bindings(
        bindings: List[Binding]
    ) -> "Environment":
        return Environment(
            bindings={
                binding.name: binding.value_or_call
                for binding in bindings
            },
            base=None,
        )


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

    @property
    def block(self) -> Block:
        return self.instruction_pointer.block

    @property
    def statement_index(self) -> int:
        return self.instruction_pointer.statement_index

    @statement_index.setter
    def statement_index(self, value) -> int:
        self.instruction_pointer.statement_index = value

    @property
    def statement(self) -> Statement:
        return self.block.statements[self.statement_index]

    @property
    def expression(self) -> Expression:
        return self.statement.expression

    @property
    def expression_term_index(self) -> int:
        return (
            self.instruction_pointer.expression_term_index
        )

    @expression_term_index.setter
    def expression_term_index(self, value) -> int:
        self.instruction_pointer.expression_term_index = (
            value
        )

    @property
    def term(self) -> Term:
        return self.expression.terms[
            self.expression_term_index
        ]


@dataclass
class FrameStack:
    frames: List[Frame]

    def push(self, frame: Frame) -> None:
        self.frames.append(frame)

    def pop(self) -> None:
        return self.frames.pop()

    def __bool__(self) -> bool:
        return bool(self.frames)

    def __len__(self) -> int:
        return len(self.frames)

    @property
    def current(self) -> Frame:
        assert self.frames
        return self.frames[-1]
