from interpret.expression import interpret_expression
from stack_machine import FrameStack
from syntax_tree import ExpressionStatement
from syntax_tree import Statement


def interpret_statement(
    frame_stack: FrameStack, statement: Statement
) -> None:
    if isinstance(statement, ExpressionStatement):
        interpret_expression_statement(
            frame_stack, statement
        )
    else:
        assert False, statement


def interpret_expression_statement(
    frame_stack: FrameStack, statement: ExpressionStatement
) -> None:
    expression = statement.expression
    interpret_expression(frame_stack, expression)
