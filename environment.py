import host.simple_call
import host.value

from itertools import chain
from stack_machine import Binding
from stack_machine import Environment
from typing import Any
from typing import List


def base_environment() -> Environment:
    return Environment.from_bindings(
        extract_all_bindings(host.simple_call, host.value)
    )


def extract_all_bindings(*modules: Any) -> List[Binding]:
    return list(
        chain.from_iterable(map(extract_bindings, modules))
    )


def extract_bindings(module: Any) -> List[Binding]:
    return [
        export
        for export in module.__dict__.values()
        if isinstance(export, Binding)
    ]
