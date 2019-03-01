import math
import sys

from host.convert import from_python
from numpy import int32
from stack_machine import Binding
from typing import Any


def value(name: str, val: Any) -> Binding:
    return Binding(name, from_python(val))


COUT = value("cout", sys.stdout.buffer)

PI = value("pi", int32(math.pi))
