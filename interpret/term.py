from stack_machine import FrameStack
from stack_machine import NumberValue
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from syntax_tree import Term


def interpret_term(frame_stack: FrameStack, term: Term):
    if isinstance(term, NumberTerm):
        interpret_number_term(frame_stack, term)
    elif isinstance(term, IdentifierTerm):
        interpret_identifier_term(frame_stack, term)
    else:
        assert False, term


def interpret_number_term(
    frame_stack: FrameStack, term: NumberTerm
):
    expression_stack = frame_stack.current.expression_stack
    expression_stack.push(NumberValue(term.value))
    next_term(frame_stack)


def interpret_identifier_term(
    frame_stack: FrameStack, term: IdentifierTerm
):
    expression_stack = frame_stack.current.expression_stack
    environment = frame_stack.current.environment
    value = environment[term.name]
    expression_stack.push(value)
    next_term(frame_stack)


def next_term(frame_stack: FrameStack):
    instruction_pointer = (
        frame_stack.current.instruction_pointer
    )
    block = instruction_pointer.block
    statement_index = instruction_pointer.statement_index
    statement = block.statements[statement_index]
    expression = statement.expression
    expression_term_index = (
        instruction_pointer.expression_term_index
    )
    if expression_term_index + 1 < len(expression.terms):
        instruction_pointer.expression_term_index += 1
    elif statement_index + 1 < len(block.statements):
        instruction_pointer.statement_index += 1
        instruction_pointer.expression_term_index = 0
    else:
        frame_stack.pop()
