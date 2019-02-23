from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from syntax_tree import Block
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class Value:
    pass


@dataclass
class NumberValue(Value):
    value: int


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
        values = []
        for _ in range(count):
            values.append(self.values.pop())
        return values


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

    def __getitem__(self, key) -> Union[Value, Call]:
        value = self.bindings.get(key)
        if value is None:
            if self.base:
                return self.base[key]
            else:
                raise KeyError(key)
        else:
            return value

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


@dataclass
class FrameStack:
    frames: List[Frame]

    def push(self, frame: Frame) -> None:
        self.frames.append(frame)

    def pop(self) -> None:
        return self.frames.pop()

    def __bool__(self) -> bool:
        return bool(self.frames)

    @property
    def current(self) -> Frame:
        assert self.frames
        return self.frames[-1]
