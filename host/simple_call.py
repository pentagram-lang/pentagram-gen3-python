import math

from dataclasses import dataclass
from dataclasses import field
from host.convert import from_python
from host.convert import to_python
from inspect import signature
from interpret.term import next_term
from io import IOBase
from numpy import int32
from numpy import integer
from stack_machine import Binding
from stack_machine import Call
from stack_machine import FrameStack
from typing import Callable


@dataclass
class SimpleHostCall(Call):
    func: Callable
    parameter_count: int = field(init=False)

    def __post_init__(self):
        self.parameter_count = len(
            signature(self.func).parameters
        )

    def __call__(self, frame_stack: FrameStack) -> None:
        frame = frame_stack.current
        expression_stack = frame.expression_stack
        args = expression_stack.pop_many(
            self.parameter_count
        )
        converted_args = [
            to_python(arg) for arg in reversed(args)
        ]
        results = self.func(*converted_args)
        if results is None:
            results = ()
        elif not isinstance(results, tuple):
            results = (results,)
        converted_results = [
            from_python(result) for result in results
        ]
        expression_stack.push_many(converted_results)
        next_term(frame_stack)


def simple_call(name: str) -> Callable[[Callable], Binding]:
    def inner(func: Callable) -> Binding:
        return Binding(name, SimpleHostCall(func))

    return inner


@simple_call("add")
def add(blob: bytearray, number: integer) -> bytearray:
    blob += number.tobytes()
    return blob


@simple_call("nil-blob")
def nil_blob() -> bytearray:
    return bytearray()


@simple_call("sqrt")
def sqrt(x: int32) -> int32:
    return int32(math.sqrt(x))


@simple_call("write")
def write(stream: IOBase, blob: bytearray) -> None:
    stream.write(blob)
