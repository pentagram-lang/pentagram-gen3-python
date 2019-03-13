from stack_machine import Call
from stack_machine import FrameStack
from stack_machine import NumberValue
from stack_machine import Value
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm


def interpret_term(frame_stack: FrameStack) -> None:
    term = frame_stack.current.term
    if isinstance(term, NumberTerm):
        interpret_number_term(frame_stack, term)
    elif isinstance(term, IdentifierTerm):
        interpret_identifier_term(frame_stack, term)
    else:
        assert False, term


def interpret_number_term(
    frame_stack: FrameStack, term: NumberTerm
) -> None:
    expression_stack = frame_stack.current.expression_stack
    expression_stack.push(NumberValue(term.value))
    next_term(frame_stack)


def interpret_identifier_term(
    frame_stack: FrameStack, term: IdentifierTerm
) -> None:
    expression_stack = frame_stack.current.expression_stack
    environment = frame_stack.current.environment
    value_or_call = environment[term.name]
    if isinstance(value_or_call, Value):
        expression_stack.push(value_or_call)
        next_term(frame_stack)
    elif isinstance(value_or_call, Call):
        value_or_call(frame_stack)
    else:
        assert False, value_or_call


def next_term(frame_stack: FrameStack) -> None:
    frame_stack.current.expression_term_index += 1
