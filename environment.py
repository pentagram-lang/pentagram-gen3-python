import math

from stack_machine import Environment
from stack_machine import NumberValue


def base_environment() -> Environment:
    return Environment(
        bindings=dict(pi=NumberValue(math.pi)), outer=None
    )
