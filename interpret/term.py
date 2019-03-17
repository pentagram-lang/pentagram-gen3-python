from machine import MachineCall
from machine import MachineFrameStack
from machine import MachineNumber
from machine import MachineValue
from syntax import SyntaxComment
from syntax import SyntaxIdentifier
from syntax import SyntaxNumber


def interpret_term(frame_stack: MachineFrameStack) -> None:
    term = frame_stack.current.term
    if isinstance(term, SyntaxNumber):
        interpret_number_term(frame_stack, term)
    elif isinstance(term, SyntaxIdentifier):
        interpret_identifier_term(frame_stack, term)
    elif isinstance(term, SyntaxComment):
        next_term(frame_stack)
    else:
        assert False, term


def interpret_number_term(
    frame_stack: MachineFrameStack, number: SyntaxNumber
) -> None:
    expression_stack = frame_stack.current.expression_stack
    expression_stack.push(MachineNumber(number.value))
    next_term(frame_stack)


def interpret_identifier_term(
    frame_stack: MachineFrameStack,
    identifier: SyntaxIdentifier,
) -> None:
    expression_stack = frame_stack.current.expression_stack
    environment = frame_stack.current.environment
    value_or_call = environment[identifier.name]
    if isinstance(value_or_call, MachineValue):
        expression_stack.push(value_or_call)
        next_term(frame_stack)
    elif isinstance(value_or_call, MachineCall):
        value_or_call(frame_stack)
    else:
        assert False, value_or_call


def next_term(frame_stack: MachineFrameStack) -> None:
    frame_stack.current.term_index += 1
