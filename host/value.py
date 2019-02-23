import math

from host.convert import from_python
from stack_machine import Binding
from typing import Any


def value(name: str, val: Any) -> Binding:
    return Binding(name, from_python(val))


PI = value("pi", int(math.pi))
