from interpret.interpret import init_frame_stack
from interpret.statement import interpret_statement
from interpret.test import init_test_frame_stack
from interpret.test import test_environment
from numpy import int32
from stack_machine import ExpressionStack
from stack_machine import NumberValue
from syntax_tree import AssignmentStatement
from syntax_tree import Block
from syntax_tree import Expression
from syntax_tree import ExpressionStatement
from syntax_tree import IdentifierTerm
from syntax_tree import NumberTerm
from syntax_tree import Statement


def init_statement_block(statement: Statement) -> Block:
    return Block([statement])


def test_interpret_expression_statement_enter():
    statement = ExpressionStatement(
        Expression(
            [NumberTerm(int32(100))],
            comment=None,
            block=None,
        )
    )
    frame_stack = init_test_frame_stack(
        init_statement_block(statement), ExpressionStack([])
    )
    interpret_statement(frame_stack)
    assert frame_stack == init_test_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(100))]),
        expression_term_index=1,
    )


def test_interpret_expression_statement_exit():
    statement = ExpressionStatement(
        Expression(
            [NumberTerm(int32(100))],
            comment=None,
            block=None,
        )
    )
    frame_stack = init_test_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(100))]),
        expression_term_index=1,
    )
    interpret_statement(frame_stack)
    assert frame_stack == init_test_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(100))]),
        statement_index=1,
        expression_term_index=0,
    )


def test_interpret_assignment_statement_1_enter():
    statement = AssignmentStatement(
        expression=Expression(
            [NumberTerm(int32(3))], comment=None, block=None
        ),
        bindings=[IdentifierTerm("x")],
    )
    frame_stack = init_test_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(4))]),
    )
    interpret_statement(frame_stack)
    assert len(frame_stack) == 2
    assert (
        frame_stack.frames[1].instruction_pointer
        is frame_stack.frames[0].instruction_pointer
    )
    assert (
        frame_stack.frames[1].environment
        is frame_stack.frames[0].environment
    )
    assert (
        frame_stack.current.expression_stack
        == ExpressionStack([NumberValue(int32(3))])
    )


def test_interpret_assignment_statement_1_exit():
    statement = AssignmentStatement(
        expression=Expression(
            [NumberTerm(int32(3))], comment=None, block=None
        ),
        bindings=[IdentifierTerm("x")],
    )
    frame_stack = init_test_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(4))]),
    )
    interpret_statement(frame_stack)
    interpret_statement(frame_stack)
    assert frame_stack == init_frame_stack(
        init_statement_block(statement),
        ExpressionStack([NumberValue(int32(4))]),
        test_environment({"x": NumberValue(int32(3))}),
        statement_index=1,
    )


def test_interpret_assignment_statement_2_exit():
    statement = AssignmentStatement(
        expression=Expression(
            [
                NumberTerm(int32(300)),
                NumberTerm(int32(400)),
            ],
            comment=None,
            block=None,
        ),
        bindings=[
            IdentifierTerm("abc"),
            IdentifierTerm("def"),
        ],
    )
    frame_stack = init_test_frame_stack(
        init_statement_block(statement), ExpressionStack([])
    )
    interpret_statement(frame_stack)
    interpret_statement(frame_stack)
    interpret_statement(frame_stack)
    assert frame_stack == init_frame_stack(
        init_statement_block(statement),
        ExpressionStack([]),
        test_environment(
            {
                "abc": NumberValue(int32(300)),
                "def": NumberValue(int32(400)),
            }
        ),
        statement_index=1,
    )
