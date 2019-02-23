import math

from dataclasses import dataclass
from dataclasses import field
from host.convert import from_python
from host.convert import to_python
from inspect import signature
from interpret.term import next_term
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
        converted_args = [to_python(arg) for arg in args]
        results = self.func(*converted_args)
        if not isinstance(results, tuple):
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


@simple_call("sqrt")
def sqrt(x: int) -> int:
    return int(math.sqrt(x))
