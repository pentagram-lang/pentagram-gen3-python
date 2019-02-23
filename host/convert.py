from stack_machine import NumberValue
from stack_machine import Value
from typing import Any


def from_python(value: Any) -> Value:
    if isinstance(value, Value):
        return value
    elif isinstance(value, int):
        return NumberValue(value)
    else:
        assert False, value


def to_python(value: Value) -> Any:
    if isinstance(value, NumberValue):
        return value.value
    elif isinstance(value, int):
        return NumberValue(value)
    else:
        assert False, value
