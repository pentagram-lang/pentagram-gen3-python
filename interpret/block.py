from interpret.statement import interpret_statement
from interpret.term import interpret_term
from stack_machine import FrameStack


def interpret_block(frame_stack: FrameStack):
    instruction_pointer = (
        frame_stack.current.instruction_pointer
    )
    block = instruction_pointer.block
    statement_index = instruction_pointer.statement_index

    statement = block.statements[statement_index]
    expression_term_index = (
        instruction_pointer.expression_term_index
    )
    if expression_term_index == 0:
        interpret_statement(frame_stack, statement)
    else:
        expression = statement.expression
        term = expression.terms[expression_term_index]
        interpret_term(frame_stack, term)
