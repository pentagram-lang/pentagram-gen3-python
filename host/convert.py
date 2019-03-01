from io import IOBase
from numpy import integer
from stack_machine import BlobValue
from stack_machine import NumberValue
from stack_machine import StreamValue
from stack_machine import Value
from typing import Any


def from_python(value: Any) -> Value:
    if isinstance(value, IOBase):
        return StreamValue(value)
    elif isinstance(value, Value):
        return value
    elif isinstance(value, bytearray):
        return BlobValue(value)
    elif isinstance(value, integer):
        return NumberValue(value)
    else:
        assert False, value


def to_python(value: Value) -> Any:
    simple_values = (BlobValue, NumberValue, StreamValue)
    if isinstance(value, simple_values):
        return value.value
    else:
        assert False, value
