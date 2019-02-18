from dataclasses import dataclass
from syntax_tree import Block
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

    def push(self, value: Value):
        self.values.append(value)

    def pop(self) -> Value:
        return self.values.pop()


@dataclass
class Environment:
    bindings: Dict[str, Value]
    base: Optional["Environment"]

    def extend(self, bindings: Dict[str, Value]):
        return Environment(bindings, base=self)

    def __getitem__(self, key):
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

    def push(self, frame: Frame):
        self.frames.append(frame)

    def pop(self):
        return self.frames.pop()

    def __bool__(self):
        return bool(self.frames)

    @property
    def current(self) -> Frame:
        assert self.frames
        return self.frames[-1]
