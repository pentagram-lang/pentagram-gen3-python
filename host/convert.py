from stack_machine import BlobValue
from stack_machine import NumberValue
from stack_machine import Value
from typing import Any


def from_python(value: Any) -> Value:
    if isinstance(value, Value):
        return value
    elif isinstance(value, bytearray):
        return BlobValue(value)
    elif isinstance(value, int):
        return NumberValue(value)
    else:
        assert False, value


def to_python(value: Value) -> Any:
    simple_values = (BlobValue, NumberValue)
    if isinstance(value, simple_values):
        return value.value
    else:
        assert False, value
