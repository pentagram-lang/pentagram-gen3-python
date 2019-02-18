import math

from stack_machine import Environment
from stack_machine import NumberValue


def base_environment() -> Environment:
    return Environment(
        bindings={"pi": NumberValue(math.pi)}, base=None
    )
