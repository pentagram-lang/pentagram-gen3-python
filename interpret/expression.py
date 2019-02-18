from interpret.term import interpret_term
from interpret.term import next_term
from stack_machine import FrameStack
from syntax_tree import Expression


def interpret_expression(
    frame_stack: FrameStack, expression: Expression
):
    if not expression.terms:
        next_term(frame_stack)
    else:
        term = expression.terms[0]
        interpret_term(frame_stack, term)
