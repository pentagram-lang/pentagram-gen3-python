from dataclasses import dataclass
from syntax_tree import Block
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class Value:
    pass


@dataclass
class NumberValue:
    value: int


@dataclass
class ExpressionStack:
    values: List[Value]

    def push(self, value: Value) -> None:
        self.values.append(value)

    def pop(self) -> Value:
        return self.values.pop()


@dataclass
class Environment:
    bindings: Dict[str, Value]
    base: Optional["Environment"]

    def extend(
        self, bindings: Dict[str, Value]
    ) -> "Environment":
        return Environment(bindings, base=self)

    def __getitem__(self, key) -> Value:
        value = self.bindings.get(key)
        if value is None:
            if self.base:
                return self.base[key]
            else:
                raise KeyError(key)
        else:
            return value


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
