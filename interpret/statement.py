from interpret.term import interpret_term
from stack_machine import ExpressionStack
from stack_machine import Frame
from stack_machine import FrameStack
from syntax_tree import AssignmentStatement
from syntax_tree import ExpressionStatement


def interpret_statement(frame_stack: FrameStack) -> None:
    expression = frame_stack.current.expression
    expression_term_index = (
        frame_stack.current.expression_term_index
    )
    if expression_term_index == 0:
        interpret_statement_enter(frame_stack)
    if expression_term_index < len(expression.terms):
        interpret_term(frame_stack)
    else:
        interpret_statement_exit(frame_stack)
        next_statement(frame_stack)


def interpret_statement_enter(
    frame_stack: FrameStack
) -> None:
    statement = frame_stack.current.statement
    if isinstance(statement, ExpressionStatement):
        pass
    elif isinstance(statement, AssignmentStatement):
        interpret_assignment_statement_enter(
            frame_stack, statement
        )
    else:
        assert False, statement


def interpret_statement_exit(
    frame_stack: FrameStack
) -> None:
    statement = frame_stack.current.statement
    if isinstance(statement, ExpressionStatement):
        pass
    elif isinstance(statement, AssignmentStatement):
        interpret_assignment_statement_exit(
            frame_stack, statement
        )
    else:
        assert False, statement


def interpret_assignment_statement_enter(
    frame_stack: FrameStack, statement: AssignmentStatement
) -> None:
    old_frame = frame_stack.current
    new_frame = Frame(
        old_frame.instruction_pointer,
        ExpressionStack([]),
        old_frame.environment,
    )
    frame_stack.push(new_frame)


def interpret_assignment_statement_exit(
    frame_stack: FrameStack, statement: AssignmentStatement
) -> None:
    expression_stack = frame_stack.current.expression_stack
    environment = frame_stack.current.environment
    for binding in reversed(statement.bindings):
        environment[binding.name] = expression_stack.pop()
    assert len(expression_stack) == 0, expression_stack
    frame_stack.pop()


def next_statement(frame_stack: FrameStack) -> None:
    frame_stack.current.statement_index += 1
    frame_stack.current.expression_term_index = 0
